import { serve } from "https://deno.land/std@0.224.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS"
};

const editableKeys = [
  "Identifier",
  "Title",
  "preferred_term",
  "legacy_title",
  "Creator",
  "Date",
  "Searchable date",
  "culture_community",
  "people_ethnolinguistic_group",
  "Geographic location",
  "place_of_creation",
  "place_of_use",
  "materials",
  "technique",
  "object_type",
  "function_use",
  "period_dynasty",
  "Subject",
  "Description",
  "provenance",
  "acquisition_context",
  "Source",
  "Notes",
  "Transcript",
  "Rights",
  "Disclaimer",
  "attribution_confidence",
  "cultural_sensitivity_note"
];

function jsonResponse(status: number, body: Record<string, unknown>) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      ...corsHeaders,
      "Content-Type": "application/json"
    }
  });
}

function parseCsv(text: string): string[][] {
  const rows: string[][] = [];
  let row: string[] = [];
  let value = "";
  let inQuotes = false;

  for (let i = 0; i < text.length; i += 1) {
    const char = text[i];
    if (inQuotes) {
      if (char === "\"") {
        if (text[i + 1] === "\"") {
          value += "\"";
          i += 1;
        } else {
          inQuotes = false;
        }
      } else {
        value += char;
      }
    } else if (char === "\"") {
      inQuotes = true;
    } else if (char === ",") {
      row.push(value);
      value = "";
    } else if (char === "\n") {
      row.push(value);
      rows.push(row);
      row = [];
      value = "";
    } else if (char !== "\r") {
      value += char;
    }
  }

  if (value !== "" || row.length) {
    row.push(value);
    rows.push(row);
  }

  return rows;
}

function csvEscape(value: unknown): string {
  const text = String(value == null ? "" : value);
  if (/[",\n]/.test(text)) {
    return `"${text.replace(/"/g, "\"\"")}"`;
  }
  return text;
}

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  if (req.method !== "POST") {
    return jsonResponse(405, { error: "Method not allowed." });
  }

  const supabaseUrl = Deno.env.get("SUPABASE_URL");
  const supabaseAnonKey = Deno.env.get("SUPABASE_ANON_KEY");
  const githubToken = Deno.env.get("GITHUB_TOKEN");
  const githubRepo = Deno.env.get("GITHUB_REPO") || "jsumsart/africanart";
  const githubBranch = Deno.env.get("GITHUB_BRANCH") || "main";
  const githubCsvPath = Deno.env.get("GITHUB_CSV_PATH") || "_data/africanart_mdl_medata.csv";
  const authHeader = req.headers.get("Authorization");

  if (!supabaseUrl || !supabaseAnonKey || !githubToken) {
    return jsonResponse(500, { error: "Missing Supabase or GitHub environment variables." });
  }

  if (!authHeader) {
    return jsonResponse(401, { error: "Missing authorization header." });
  }

  const supabase = createClient(supabaseUrl, supabaseAnonKey, {
    global: {
      headers: {
        Authorization: authHeader
      }
    }
  });

  const userResponse = await supabase.auth.getUser();
  if (userResponse.error || !userResponse.data.user) {
    return jsonResponse(401, { error: "Staff sign-in is required before write-back can continue." });
  }

  const user = userResponse.data.user;

  let payload: {
    objectName?: string;
    commitMessage?: string;
    updates?: Record<string, string>;
  };
  try {
    payload = await req.json();
  } catch {
    return jsonResponse(400, { error: "Request body must be valid JSON." });
  }

  const objectName = String(payload.objectName || "").trim();
  const commitMessage = String(payload.commitMessage || "").trim() || `Update ${objectName} metadata`;
  const updates = payload.updates || {};

  if (!objectName) {
    return jsonResponse(400, { error: "An object identifier is required." });
  }

  const fileResponse = await fetch(`https://api.github.com/repos/${githubRepo}/contents/${encodeURIComponent(githubCsvPath)}`, {
    headers: {
      "Accept": "application/vnd.github+json",
      "Authorization": `Bearer ${githubToken}`
    }
  });

  if (!fileResponse.ok) {
    return jsonResponse(502, { error: `GitHub file fetch failed (${fileResponse.status}).` });
  }

  const file = await fileResponse.json();
  const csvText = new TextDecoder().decode(Uint8Array.from(atob(file.content.replace(/\n/g, "")), (char) => char.charCodeAt(0)));
  const rows = parseCsv(csvText);
  const headers = rows[0] || [];
  const objectNameIndex = headers.indexOf("Object name");

  if (objectNameIndex === -1) {
    return jsonResponse(500, { error: "The master CSV does not contain an Object name column." });
  }

  const rowIndex = rows.findIndex((row, index) => index > 0 && row[objectNameIndex] === objectName);
  if (rowIndex === -1) {
    return jsonResponse(404, { error: `Could not find ${objectName} in the master CSV.` });
  }

  editableKeys.forEach((key) => {
    const headerIndex = headers.indexOf(key);
    if (headerIndex > -1) {
      rows[rowIndex][headerIndex] = String(updates[key] || "");
    }
  });

  const nextCsv = rows.map((row) => headers.map((_, index) => csvEscape(row[index] || "")).join(",")).join("\n") + "\n";
  const encoded = btoa(String.fromCharCode(...new TextEncoder().encode(nextCsv)));

  const commitResponse = await fetch(`https://api.github.com/repos/${githubRepo}/contents/${encodeURIComponent(githubCsvPath)}`, {
    method: "PUT",
    headers: {
      "Accept": "application/vnd.github+json",
      "Authorization": `Bearer ${githubToken}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      message: commitMessage,
      content: encoded,
      sha: file.sha,
      branch: githubBranch
    })
  });

  if (!commitResponse.ok) {
    return jsonResponse(502, { error: `GitHub commit failed (${commitResponse.status}).` });
  }

  const commitResult = await commitResponse.json();

  await supabase.from("catalog_edit_audit").insert({
    user_id: user.id,
    user_email: user.email,
    object_name: objectName,
    commit_message: commitMessage,
    commit_sha: commitResult.commit?.sha || null,
    payload: updates
  });

  return jsonResponse(200, {
    ok: true,
    objectName,
    commitSha: commitResult.commit?.sha || null,
    message: "Catalog update committed to GitHub. GitHub Pages will refresh the public site after the deploy finishes."
  });
});

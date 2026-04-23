import { serve } from "https://deno.land/std@0.224.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

const csvHeaders = [
  "Object name",
  "Identifier",
  "Alternate ID",
  "Title",
  "Alternate title(s)",
  "Replaces",
  "Replaced by",
  "Description",
  "Creator",
  "Searchable date",
  "Date",
  "Coverage (time period)",
  "Time period",
  "Subject",
  "Mississippi county",
  "Geographic location",
  "Resource type",
  "Format",
  "Media format",
  "Language",
  "Language code",
  "Publisher",
  "Contributors",
  "Notes",
  "Rights",
  "Disclaimer",
  "Contributing institution",
  "Collection",
  "Source",
  "Digital repository",
  "Digital collection",
  "File size",
  "File extension",
  "Width",
  "Height",
  "Color space",
  "Date digital",
  "Capture method",
  "Processing software",
  "Master image",
  "Record created by",
  "Hidden notes",
  "Custom searches",
  "IP resolution",
  "Transcript",
  "File name",
  "culture_community",
  "people_ethnolinguistic_group",
  "place_of_creation",
  "place_of_use",
  "materials",
  "technique",
  "object_type",
  "function_use",
  "period_dynasty",
  "provenance",
  "acquisition_context",
  "preferred_term",
  "legacy_title",
  "attribution_confidence",
  "cultural_sensitivity_note",
  "youtubeid",
  "vimeoid",
  "latitude",
  "longitude",
  "format",
];

function jsonResponse(status, body) {
  return new Response(JSON.stringify(body), {
    status: status,
    headers: {
      ...corsHeaders,
      "Content-Type": "application/json",
    },
  });
}

function csvEscape(value) {
  const text = String(value == null ? "" : value);
  if (/[",\n]/.test(text)) {
    return `"${text.replace(/"/g, "\"\"")}"`;
  }
  return text;
}

function csvRow(values) {
  return values.map(function (value) {
    return csvEscape(value);
  }).join(",");
}

function toBase64(text) {
  const bytes = new TextEncoder().encode(text);
  let binary = "";
  for (let i = 0; i < bytes.length; i += 1) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary);
}

serve(async function (req) {
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
        Authorization: authHeader,
      },
    },
  });

  const userResponse = await supabase.auth.getUser();
  if (userResponse.error || !userResponse.data.user) {
    return jsonResponse(401, { error: "Staff sign-in is required before publishing can continue." });
  }

  const user = userResponse.data.user;
  let payload = {};
  try {
    payload = await req.json();
  } catch (_error) {
    payload = {};
  }

  const saveMessage = String(payload.saveMessage || "Publish updated catalog snapshot").trim();

  const recordsResponse = await supabase
    .from("catalog_records")
    .select("object_name,title,culture_community,geographic_location,file_name,asset_format,record")
    .order("object_name", { ascending: true });

  if (recordsResponse.error) {
    return jsonResponse(500, { error: recordsResponse.error.message });
  }

  const rows = (recordsResponse.data || []).map(function (row) {
    const record = Object.assign({}, row.record || {});
    record["Object name"] = row.object_name || record["Object name"] || "";
    record["Title"] = row.title || record["Title"] || "";
    record["Geographic location"] = row.geographic_location || record["Geographic location"] || "";
    record["culture_community"] = row.culture_community || record["culture_community"] || "";
    record["File name"] = row.file_name || record["File name"] || "";
    record["format"] = row.asset_format || record["format"] || "";

    return csvRow(csvHeaders.map(function (header) {
      return record[header] || "";
    }));
  });

  const nextCsv = csvRow(csvHeaders) + "\n" + rows.join("\n") + "\n";
  const githubUrl = "https://api.github.com/repos/" + githubRepo + "/contents/" + encodeURIComponent(githubCsvPath);

  const fileResponse = await fetch(githubUrl, {
    headers: {
      Accept: "application/vnd.github+json",
      Authorization: "Bearer " + githubToken,
    },
  });

  if (!fileResponse.ok) {
    return jsonResponse(502, { error: "GitHub file fetch failed (" + fileResponse.status + ")." });
  }

  const file = await fileResponse.json();
  const encodedCsv = toBase64(nextCsv);

  const commitResponse = await fetch(githubUrl, {
    method: "PUT",
    headers: {
      Accept: "application/vnd.github+json",
      Authorization: "Bearer " + githubToken,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message: saveMessage,
      content: encodedCsv,
      sha: file.sha,
      branch: githubBranch,
    }),
  });

  if (!commitResponse.ok) {
    return jsonResponse(502, { error: "GitHub publish failed (" + commitResponse.status + ")." });
  }

  const commitResult = await commitResponse.json();

  await supabase.from("catalog_edit_audit").insert({
    user_id: user.id,
    user_email: user.email,
    object_name: String(payload.objectName || ""),
    save_message: saveMessage,
    publish_sha: commitResult.commit && commitResult.commit.sha ? commitResult.commit.sha : null,
    payload: payload,
  });

  return jsonResponse(200, {
    ok: true,
    publishSha: commitResult.commit && commitResult.commit.sha ? commitResult.commit.sha : null,
    message: "Live catalog snapshot published to GitHub. GitHub Pages will refresh the public site after the deploy finishes.",
  });
});

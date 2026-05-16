const crypto = require("crypto");

function json(statusCode, body) {
  return {
    statusCode,
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "Content-Type",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
    },
    body: JSON.stringify(body),
  };
}

function sha256(value) {
  return crypto.createHash("sha256").update(value).digest("hex");
}

async function dispatchWorkflow(payload) {
  const owner = process.env.GITHUB_OWNER || "jsumsart";
  const repo = process.env.GITHUB_REPO || "africanart";
  const workflowId =
    process.env.GITHUB_WORKFLOW_ID || "catalog-room-save.yml";
  const workflowToken = process.env.GITHUB_WORKFLOW_TOKEN;
  const ref = process.env.GITHUB_WORKFLOW_REF || "main";

  if (!workflowToken) {
    throw new Error("GitHub workflow token is not configured.");
  }

  const response = await fetch(
    `https://api.github.com/repos/${owner}/${repo}/actions/workflows/${workflowId}/dispatches`,
    {
      method: "POST",
      headers: {
        Accept: "application/vnd.github+json",
        Authorization: `Bearer ${workflowToken}`,
        "Content-Type": "application/json",
        "User-Agent": "jsu-african-art-catalog-room",
      },
      body: JSON.stringify({
        ref,
        inputs: payload,
      }),
    }
  );

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`GitHub workflow dispatch failed: ${text}`);
  }
}

exports.handler = async function (event) {
  if (event.httpMethod === "OPTIONS") {
    return json(200, { ok: true });
  }

  if (event.httpMethod !== "POST") {
    return json(405, { message: "Method not allowed." });
  }

  try {
    const expectedPasswordHash = process.env.EDITOR_PASSWORD_SHA256 || "";
    if (!expectedPasswordHash) {
      return json(500, { message: "Editor password hash is not configured." });
    }

    const body = JSON.parse(event.body || "{}");
    const editorEmail = String(body.editor_email || "").trim();
    const editorPassword = String(body.editor_password || "");
    const editorSessionHash = String(body.editor_session_hash || "");
    const saveActionType = String(body.save_action_type || "").trim();
    const commitMessage = String(body.commit_message || "").trim();
    const record = body.record || null;
    const settings = body.settings || null;

    if (!editorEmail || (!editorPassword && !editorSessionHash)) {
      return json(400, {
        message: "Editor email and editor authorization are required.",
      });
    }

    const providedHash = editorSessionHash || sha256(editorPassword);
    if (providedHash !== expectedPasswordHash) {
      return json(401, { message: "Editor credentials were not recognized." });
    }

    if (saveActionType !== "record" && saveActionType !== "settings") {
      return json(400, {
        message: "save_action_type must be 'record' or 'settings'.",
      });
    }

    if (saveActionType === "record" && !record) {
      return json(400, { message: "A record payload is required." });
    }

    if (saveActionType === "settings" && !settings) {
      return json(400, { message: "A settings payload is required." });
    }

    await dispatchWorkflow({
      save_action_type: saveActionType,
      editor_email: editorEmail,
      commit_message:
        commitMessage ||
        (saveActionType === "record"
          ? `Save catalog record from Catalog Room (${editorEmail})`
          : `Save site settings from Catalog Room (${editorEmail})`),
      record_json: saveActionType === "record" ? JSON.stringify(record) : "",
      settings_json:
        saveActionType === "settings" ? JSON.stringify(settings) : "",
    });

    return json(202, {
      ok: true,
      message:
        "Save request accepted. GitHub is processing the update and the site will refresh after Pages rebuilds.",
    });
  } catch (error) {
    return json(500, {
      message: error.message || "The save request could not be processed.",
    });
  }
};

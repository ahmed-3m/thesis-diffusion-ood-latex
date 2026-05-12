import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const endpoint = "https://api.languagetool.org/v2/check";
const files = process.argv.slice(2);
const targets = files.length > 0
  ? files
  : fs.readdirSync(root).filter((file) => /^\d{2}-.+\.tex$/.test(file) || /^9\d-appendix-.+\.tex$/.test(file));

function texToPlainText(input) {
  return input
    .replace(/%.*$/gm, "")
    .replace(/\\(?:citep?|textcite|ref|label|url|href)(?:\[[^\]]*\])?\{[^}]*\}/g, " ")
    .replace(/\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{([^{}]*)\})?/g, "$1")
    .replace(/\$[^$]*\$/g, " ")
    .replace(/[{}]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function chunkText(text, size = 12000) {
  const chunks = [];
  for (let start = 0; start < text.length; start += size) {
    chunks.push(text.slice(start, start + size));
  }
  return chunks;
}

let totalMatches = 0;
const ignoredCategories = new Set(["TYPOS", "TYPOGRAPHY", "CASING", "PUNCTUATION"]);
const ignoredRules = new Set([
  "MORFOLOGIK_RULE_EN_GB",
  "OXFORD_SPELLING_Z_NOT_S",
  "WHITESPACE_RULE",
  "EN_UNPAIRED_BRACKETS",
  "CURRENCY"
]);

for (const file of targets) {
  const fullPath = path.join(root, file);
  const text = texToPlainText(fs.readFileSync(fullPath, "utf8"));
  const chunks = chunkText(text);

  for (let i = 0; i < chunks.length; i += 1) {
    const body = new URLSearchParams({
      text: chunks[i],
      language: "en-GB",
      enabledOnly: "false"
    });

    const response = await fetch(endpoint, {
      method: "POST",
      headers: { "content-type": "application/x-www-form-urlencoded" },
      body
    });

    if (!response.ok) {
      throw new Error(`LanguageTool request failed for ${file} chunk ${i + 1}: ${response.status} ${response.statusText}`);
    }

    const result = await response.json();
    const matches = result.matches.filter((match) => {
      const category = match.rule?.category?.id;
      const ruleId = match.rule?.id;
      return !ignoredCategories.has(category) && !ignoredRules.has(ruleId);
    });
    totalMatches += matches.length;

    for (const match of matches.slice(0, 25)) {
      const replacement = match.replacements?.[0]?.value ? ` Suggestion: ${match.replacements[0].value}` : "";
      console.log(`${file}: ${match.message}${replacement}`);
    }
  }
}

if (totalMatches > 0) {
  console.error(`\nLanguageTool found ${totalMatches} potential issue(s). Review manually before editing.`);
  process.exit(1);
}

console.log("LanguageTool check passed.");

import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const files = fs.readdirSync(root).filter((file) => /^\d{2}-.+\.tex$/.test(file) || /^9\d-appendix-.+\.tex$/.test(file));

const patterns = [
  [/it is important to note/gi, "generic academic filler"],
  [/it is worth noting/gi, "generic academic filler"],
  [/delve into/gi, "AI-like phrasing"],
  [/plays a crucial role/gi, "overused phrasing"],
  [/robust and comprehensive/gi, "over-smoothed phrasing"],
  [/underscore(?:s)? the importance/gi, "generic conclusion phrasing"],
  [/in the realm of/gi, "AI-like phrasing"],
  [/this showcases/gi, "generic AI-style verb"],
  [/cutting-edge/gi, "unsupported hype"],
  [/state-of-the-art solution/gi, "unsupported hype"],
  [/proprietary/gi, "forbidden reproducibility wording"],
  [/not publicly released/gi, "forbidden reproducibility wording"],
  [/limiting external reproducibility/gi, "forbidden reproducibility wording"],
  [/not publicly available/gi, "forbidden reproducibility wording"],
  [/Food-101/gi, "removed non-retained dataset"],
  [/STL-10/gi, "removed non-retained dataset"]
];

let findings = 0;

for (const file of files) {
  const fullPath = path.join(root, file);
  const lines = fs.readFileSync(fullPath, "utf8").split(/\r?\n/);
  lines.forEach((line, index) => {
    for (const [pattern, reason] of patterns) {
      pattern.lastIndex = 0;
      if (pattern.test(line)) {
        findings += 1;
        console.log(`${file}:${index + 1}: ${reason}: ${line.trim()}`);
      }
    }
  });
}

if (findings > 0) {
  console.error(`\nAI-style/reproducibility check found ${findings} issue(s).`);
  process.exit(1);
}

console.log("AI-style/reproducibility check passed.");

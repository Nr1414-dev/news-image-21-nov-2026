// news-image-20261121 entrypoint: put the pre-drawn front page where the
// grader reads it. The picture is a fixed file shipped in this repository,
// so each run emits byte-identical output with no network and no randomness.
import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { join } from "node:path";

const repoRoot = new URL(".", import.meta.url).pathname;
const destination = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(destination, { recursive: true });
const source = join(repoRoot, "entry.png");
const target = join(destination, "entry.png");
copyFileSync(source, target);
const bytes = statSync(target).size;
if (bytes > 1048576) {
  throw new Error(`entry.png is ${bytes} bytes, over the 1 MiB cap`);
}

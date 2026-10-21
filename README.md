# Repo Secrets Scanner (lite)

## English

### Purpose

A free slice of the scanner: three known shapes (AWS access key id, GitHub `ghp_`, and a PEM private-key header) and a small walker that redacts matches. The lite subset has no entropy pass, no allowlist, and no Slack or Stripe patterns. Fixtures are fake and carry `EXAMPLE` or `FAKE`.

### Deliverables

- `deliverables/scan_patterns.py` — pattern-only scanner.
- `deliverables/patterns.json` — the three patterns above. Confirm prefixes in the upstream docs named in each note.
- `examples/fixtures/hit_aws.env` — fake access key id ending in `EXAMPLE`.
- `examples/fixtures/hit_github.txt` — fake `ghp_` token whose body is `FAKE`.
- `examples/fixtures/hit_pem.txt` — PEM header that contains the word `FAKE`.
- `examples/fixtures/miss_prose.md` — prose with `ops@example.com` and `192.0.2.10`. No hit.
- `examples/fixtures/miss_low_entropy.txt` — low-entropy strings. This subset does not score entropy, so they are simply not pattern hits.

### Quick start

```bash
python3 deliverables/scan_patterns.py --root examples/fixtures/hit_aws.env
python3 deliverables/scan_patterns.py --root examples/fixtures/miss_prose.md
```

Exit code 0 means no hits. Exit code 1 means at least one hit. Stdout prints `redacted=` values. The program does not open a socket. Python 3.9 or newer, standard library only.

## 中文

### 用途

扫描器的免费子集：三种已知形状（AWS 访问密钥 ID、GitHub `ghp_`、PEM 私钥头）和一个会打码的小型遍历器。免费子集没有熵检查，没有允许清单，也没有 Slack 或 Stripe 模式。夹具是假的，带有 `EXAMPLE` 或 `FAKE`。

### 交付清单

- `deliverables/scan_patterns.py` — 只做模式匹配的扫描器。
- `deliverables/patterns.json` — 上面三种模式。每条说明里点名的上游文档，用来核对前缀。
- `examples/fixtures/hit_aws.env` — 以 `EXAMPLE` 结尾的假访问密钥 ID。
- `examples/fixtures/hit_github.txt` — 主体是 `FAKE` 的假 `ghp_` 记号。
- `examples/fixtures/hit_pem.txt` — 含有单词 `FAKE` 的 PEM 头。
- `examples/fixtures/miss_prose.md` — 含 `ops@example.com` 和 `192.0.2.10` 的普通文字。不应命中。
- `examples/fixtures/miss_low_entropy.txt` — 低熵字符串。这个子集不算熵，所以它们只是不匹配模式。

### 快速开始

```bash
python3 deliverables/scan_patterns.py --root examples/fixtures/hit_aws.env
python3 deliverables/scan_patterns.py --root examples/fixtures/miss_prose.md
```

退出码 0 表示没有命中。退出码 1 表示至少一条命中。标准输出是 `redacted=` 的值。程序不打开套接字。需要 Python 3.9 或更新版本，只要标准库。

Full version: GUMROAD_URL

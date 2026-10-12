# AgentForge スキルレビュー（2026-10-12）

対象は `skills/` の5スキル、参照ファイル・補助スクリプト、プラットフォーム別の指示、導入経路。`skill-review` と `skill-creator` の観点で内部矛盾と実行可能性を確認した。

## 良い点

- `lean-routing` の「A single trivial command should normally be run directly」は、単純操作で委譲コストを増やさない明確な判断基準になっている。
- `scientific-debugging` の「NEVER touch production/application code until ... a minimal ... reproduction test ... FAILS」は、非自明な不具合に推測で修正を重ねることを防ぐ。Fast-Path が失敗した場合の Strict Gate への移行も明示されている。
- スキルは個別の `SKILL.md`、`references/`、`scripts/`、`templates/` に分かれ、各定義は500行未満。モデル設定はアダプターに分離されている。

## 優先度順の指摘と対応

| 優先度 | 場所 | 問題 | 対応 |
|---|---|---|---|
| BLOCKER | `skills/pr-guardian/scripts/scan_diff.py:main` | Windows の既定文字コードで UTF-8 の差分を読めず、「変更なし」と誤報。Git エラーも無視 | UTF-8 と明示的な終了コード確認を追加。両方の回帰テストで Red → Green を確認 |
| BLOCKER | `scripts/validate.py:main` | Windows でも Bash に Windows パスを渡し、導入検証が失敗 | Windows は PowerShell、その他は Bash を使用。既存指示保持・再導入・解除の往復テストで Red → Green を確認 |
| SHOULD FIX | `spec-driven-dev/SKILL.md` の Core Principles、各アダプターの Spec/Debugging 指示 | 常時 Red-First と即時修正 Fast-Path の優先関係が不明 | 根拠のある1行修正だけ Fast-Path を優先。文書変更は文書検査と明記 |
| SHOULD FIX | `scientific-debugging/references/debugging-protocol.md` の Fast-Path Criteria | 本体は1–2行、参照は1–3行、AGENTS は1行 | 1行に統一し、修正前の仮説提示を明記 |
| SHOULD FIX | 各 `SKILL.md` の Delegation、`lean-routing` の R2 | 各工程の委譲指定が、単純操作は直接実行する原則と衝突 | 工程の担当は推奨と明記。R0/R1を優先し、委譲不可の場合の対応を定義 |
| SHOULD FIX | `AGENTS.md` の Cost-aware routing、`lean-routing/SKILL.md` | 配布スキル名は `lean-routing` だがルート指示は Gemini 専用名。Codex の担当名はアンダースコア | 共通名を入口にし、旧 Gemini 名の適用条件・Codex の名称対応を明記 |
| SHOULD FIX | `pr-guardian/templates/pr-manifest.md` の Verification | 検証前から全項目が `[x]` | 全項目を未チェックに変更し、証拠がある項目だけ確認済みにする |
| SHOULD FIX | `pr-guardian` の Core Principles、hygiene-rules、scanner 表示 | 正常な CLI 出力もデバッグ扱いし、限定パターン検査を秘密情報ゼロの証明にしていた | 一時的デバッグと正常な出力を区別。未追跡ファイル・検査限界を明記し、成功表示を限定 |
| SHOULD FIX | 各 `SKILL.md` の Resources | 補助スクリプトの実行方法、参照・テンプレートの利用時点が不足 | 呼び出し方法と必要なときに読む条件を追記 |
| SHOULD FIX | cartographer、spec、PR の frontmatter description | 自然な利用要求と適用条件が弱い | 探索、機能実装、出荷前レビューなどの具体的条件を記載 |

## 受け入れ条件と修正境界

- Given: Windows の作業環境。When: 検証を実行。Then: ネイティブの導入処理で3アダプターの往復検証が成功し、元の指示が残る。
- Given: UTF-8 の差分と追加された breakpoint。When: PR scanner を実行。Then: 差分を検査し終了コード1で検出する。
- Given: Git リポジトリ外。When: PR scanner を実行。Then: 検査失敗を終了コード2で報告し、clean と判定しない。
- Given: 単純操作・利用不可の担当・軽微なバグ修正。When: スキルを適用。Then: 実行方法と規則の優先関係が定まる。

コード修正は `scripts/validate.py` と `skills/pr-guardian/scripts/scan_diff.py`。回帰テストは `tests/test_validation.py` と `tests/test_pr_guardian.py`。その他の修正は `AGENTS.md`、5つの `SKILL.md`、関連する TDD・debugging・hygiene の参照、PR テンプレート、3アダプターの指示断片、`docs/install.md`、`docs/platforms.md`、本記録に限定した。既存モデル設定を維持した。

原因仮説は、導入検証では OS に関係なく Bash を選択していたこと、PR scanner では既定文字コードを用い Git の失敗を無視していたこと。OS に合った呼び出し、UTF-8 の明示、失敗の伝播が各再現を成功させた。

## 検証と影響範囲

- `python -m unittest discover -s tests -v`: 当初3テスト成功。リモート統合後は既存の allow-print 検証も含む10テスト成功。各不具合は修正前に期待した理由で失敗することも確認。
- `scripts/validate.py` は上記テストから実行し、3アダプターの導入・再導入・既存指示保持・解除を一時ディレクトリで検証。
- skill-creator の `quick_validate.py` は `python -X utf8` で5スキルを検査。Windows の通常起動は補助ツール自身の既定文字コードで失敗するため、UTF-8 モードを使用。
- `git diff --check` と PR scanner で差分を検査。新規テストと本記録は別途確認。
- 当初の PR scanner の終了コード1は scanner 自身の正常な CLI 結果表示への一致1件。リモート追加の `--allow-print` を統合し、正常出力ファイルだけ明示的に許可して再検査する。秘密情報や breakpoint はこの許可の対象外。
- `rg` による呼び出し確認: `validate.py` は CI・package.py・README・導入文書・回帰テストから参照。`scan_diff.py` は PR スキル・回帰テストから参照。アダプター指示はインストーラーが配布する。

Linux/macOS の実行と、有料モデルを呼ぶ実際の委譲は未検証。ローカルのモデル一覧では既存 Codex モデル名を確認したが、呼び出し成功を保証するものではない。PR scanner は追跡済み差分の限定パターン検査であり、包括的な秘密情報検査ではない。境界チェッカーは複雑なパス・rename・既存変更がある場合、Git の実際の状態も確認する。

Codex のスキル発見場所と設定形式は [Build skills](https://learn.chatgpt.com/docs/build-skills) と [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) で確認した。

## リモート更新との統合

未取り込みだった `25512f7`（uv/ruff、コードサイズ規則、スキルの Tools 案内、print 許可設定）を fast-forward で取り込み、8ファイルの競合を解消。リモートの分割済み検証関数と `scan` / `read_diff` / `--allow-print` を残し、Windows 対応と失敗伝播をその構造に適用した。双方のテストを保持した。

この環境には `make` がないため、Ruff lint・format、ShellCheck、コードサイズ検査、unittest、導入検証を直接実行する。Ruff・format・ShellCheck・コードサイズ検査は成功。`uv sync --locked` は OS の証明書ストアを使う `--native-tls` で実行した。同期前の差分と stash は `.git/agentforge-sync-backup-20261012-215028/` に記録し、stash `281d8956850ab5a50ff152af0a52052df193ba9b` も保持している。

## 利用

このリポジトリでは `.\installers\install.ps1 codex .` を実行し、5スキルを `.agents/skills/`、4担当設定を `.codex/agents/` に配置済み。スキル本体のコピー一致と指示ブロックが1つだけであることを確認した。配置先はこのリポジトリの `.gitignore` に従い追跡対象外。

`$lean-routing`、`$codebase-cartographer`、`$scientific-debugging`、`$spec-driven-dev`、`$pr-guardian` の名前で呼び出す。表示されない場合は Codex を再起動する。別のリポジトリには `docs/install.md` の導入手順を使う。

## 追加レビュー（2026-10-12）

実際のスキル補助スクリプトを一時Gitリポジトリでも実行し、手順を守ったまま誤判定するケースを確認した。今回の変更はレビュー記録だけで、スキル本体は未変更。

| 優先度 | 場所 | 確認した問題 | 改善案 |
|---|---|---|---|
| BLOCKER | `skills/spec-driven-dev/scripts/check_boundary.py:12-22,34-35` | 人間向けporcelainを行で分割するため、スペース・日本語名の追跡変更を許可リスト内でも逸脱扱いする。renameは移動先しか検査せず、許可外の元ファイル削除を見落とす。既存のユーザー変更も課題開始時のbaselineなしでは逸脱扱いする。 | `--porcelain=v1 -z`をNUL区切りで解析し、renameの両側を検査する。開始時baselineとの差分だけを境界判定し、事前変更にはrestoreを促さない。スペース・日本語・rename・事前変更を回帰テストする。 |
| BLOCKER | `skills/pr-guardian/scripts/scan_diff.py:30-40,94-96` | 現在のHEADとの差だけを見るので、既にcommitしたブランチ変更はpush/PR前でも「差分なし」で通る。手元のcommit前検査としては有用でも、PR出荷前検査の説明を満たさない。 | PR baseを指定してmerge-baseからHEADまで検査するモードを追加し、base不明・fetch不足ならclean扱いしない。ステージ済み/作業中検査とはモードを分ける。commit済みbreakpointの再現を追加する。 |
| SHOULD FIX | `skills/scientific-debugging/scripts/verify_repro.py:20-32` | `--expect-failure -- <存在しないコマンド>`もexit code 1だけで再現成功と表示する。非ゼロだけでは対象バグ・test assertion・実行環境エラーを区別できない。失敗を確認するcheckerと、根因を確認する人間の作業が混同される。 | 実行不能とテスト失敗を区別し、期待する終了コードまたはstderr条件を指定可能にする。テスト名/失敗アサーションを確認してからPASSにする。存在しない実行ファイルと、既知の失敗テストを別々に検査する。 |
| SHOULD FIX | `skills/codebase-cartographer/scripts/generate_map.py:75-78,101-107,111-114` | 先頭ドットのディレクトリ・ファイルを一律除外するので`.github/workflows`等が地図に出ない。シンボルは最大6件だけ表示し、省略を示さない。存在しない入力パスも空の地図をexit 0で出す。 | Git管理対象や関連設定を含むinventoryへ変更し、依存物・秘密情報は明示パターンで除外する。省略数を表示し、存在しないrootは失敗にする。長大・binary fileを全文読まず上限を設ける。 |
| SHOULD FIX | `skills/codebase-cartographer/SKILL.md:38-39`、`skills/lean-routing/scripts/route_task.py:11-31` | Cartographerは「architectureを含む探索」をgenerate_mapへ直接送るとするが、keyword routerは`architecture`をL4 parentへ送る。`overview`はL1、その他の日本語表現はfallbackになり、同じ依頼でも説明とtriage結果が一致しない。 | L0の機械的な構造抽出と、結果を解釈するparent/worker判断を別段階として明記する。説明中のautomatic routing claimを削り、誤誘導語・日本語依頼・二語混在のrouter testを追加する。 |
| CONSIDER | `skills/spec-driven-dev/SKILL.md:40,59`、`skills/scientific-debugging/SKILL.md:74` | 再利用できるガイドがあらゆる機能でfull suiteとmanifestを必須にし、debuggingはregressionなしを保証すると記述する。一方lean-routingは影響に応じたtargeted verificationを薦める。大規模repoでは毎回高コストで、suite実行から無回帰を保証するとの表現も強い。 | projectの必須品質gateを優先しつつ、対象テスト→必要時に広いsuiteという段階を説明する。manifestはプロジェクト要件または複数工程で必要な場合に保存し、no-regressionsは実行したcoverageの範囲に限定する。 |

優先着手はboundary parser、PR base比較、repro checkerの3件。cartographerとrouterの修正は、その後に小さい一貫した変更として扱う。上記は未実装の改善提案であり、この追補でスキルの実行可否や既存の検証実績を書き換えてはいない。

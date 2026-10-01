# 成績報表的分享與 CI/CD 範例

第九章重寫版使用的獨立專案，承接第七章完成後的報表：92、91、87，平均 90.0。新增驗證工具與 GitHub Actions，原第七章報表專案保留。

教材：[第九章重寫版](../../ch09-rewrite/README.md)。

## 直接使用已有 Image

```bash
docker image inspect python-report:1.1
docker tag python-report:1.1 USERNAME/python-report:1.1
```

把 USERNAME 換成小寫 Docker Hub 帳號。原 Image 若已清理，才在本目錄執行 `docker build -t python-report:1.1 .` 補建。不重做 CSV 更新或版本比較。

## 檔案

| 檔案 | 用途 |
|---|---|
| `read_scores.py`、`data/evaluation.csv`、`Dockerfile` | 第七章完成後的報表，供 CI 重建 |
| `verify.py` | 執行指定 Image，對照目前 CSV 檢查輸出 |
| `.github/workflows/report.yml` | main／PR 自動驗證、版本 Git Tag 自動發布 |

主機有 Python 時可選做 `python3 verify.py python-report:1.1`。只需標準函式庫。報表本身在 Container 執行，不需主機 Python。

## 進階選做：CI 錯誤練習

在 PR 故意把分母改成筆數加一。程式仍能執行，但平均會從 90.0 變成 67.5，CI 驗證應失敗。修正同一個 PR 後通過，不另外建置錯誤版本或重做本機回滾。

## 進階選做：CD 發布

以本目錄為 GitHub Repository 根目錄。main Push 和 PR 只驗證，Push `v1.2` 則在測試通過後發布 Docker Hub `1.2`。這次報表內容仍為 90.0，重點是從手動發布改為自動。

需建立 Docker Hub `USERNAME/python-report`，並在 GitHub Actions Secrets 設定 `DOCKERHUB_USERNAME`、有發布權限的 `DOCKERHUB_TOKEN`。Token 不寫入專案檔案。

測試 Image 經 docker save、Artifact、docker load 傳給發布 Job，不重新 Build。自動發布不移動 latest，也不覆蓋已發布版本。Image 是單平台 Build，分享時需確認目標相容。

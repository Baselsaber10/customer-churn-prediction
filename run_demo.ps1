.\venv\Scripts\Activate.ps1
pip install -r deploy\requirements.txt

Write-Host "`n--- Running MLFlow tracking to retrain model ---"
python mlops\train_track.py

Write-Host "`n--- Starting FastAPI application in the background ---"
$apiProcess = Start-Process -FilePath "python" -ArgumentList "-m uvicorn deploy.app:app --port 8000" -PassThru -NoNewWindow
Start-Sleep -Seconds 5

Write-Host "`n--- Testing the API with dummy requests ---"
python test_api.py

Write-Host "`n--- Generating Data Drift Report ---"
python monitoring\data_drift_report.py

Write-Host "`n--- Stopping FastAPI application ---"
Stop-Process -Id $apiProcess.Id -Force

Write-Host "`nAll manual tests completed successfully!"

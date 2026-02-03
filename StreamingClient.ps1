# InteractiveStreamingClient.ps1

# The endpoint URL
$Url = "http://127.0.0.1:8000/run-task-stream"

Write-Host "=== Agentic AI Interactive Client ==="
Write-Host "Type your query and press Enter. Type 'exit' to quit.`n"

while ($true) {
    # Get user query
    $UserQuery = Read-Host "Enter your query"
    if ($UserQuery.ToLower() -eq "exit") { break }

    # Prepare JSON body
    $Body = @{
        user_query = $UserQuery
    } | ConvertTo-Json

    # Create web request
    $Request = [System.Net.WebRequest]::Create($Url)
    $Request.Method = "POST"
    $Request.ContentType = "application/json"
    $Request.Accept = "text/plain"

    # Write JSON to request
    $Bytes = [System.Text.Encoding]::UTF8.GetBytes($Body)
    $Request.ContentLength = $Bytes.Length
    $RequestStream = $Request.GetRequestStream()
    $RequestStream.Write($Bytes, 0, $Bytes.Length)
    $RequestStream.Close()

    # Get response stream
    $Response = $Request.GetResponse()
    $Stream = $Response.GetResponseStream()
    $Reader = New-Object System.IO.StreamReader($Stream)

    Write-Host "`n--- Streaming Response ---`n"

    # Read line by line as it streams
    while (-not $Reader.EndOfStream) {
        $Line = $Reader.ReadLine()
        if ($Line) { Write-Host $Line }
    }

    Write-Host "`n--- End of Response ---`n"

    # Cleanup
    $Reader.Close()
    $Stream.Close()
    $Response.Close()
}

Write-Host "`nExiting Agentic AI Client. Goodbye!`n"

from zapv2 import ZAPv2

# Configure OWASP ZAP
zap = ZAPv2()

# Define your target URL
target = 'https://staging.furaha.financial'

# Spider the target URL
print('Spidering target %s' % target)
zap.spider.scan(target)

# Give ZAP time to start the spider
time.sleep(2)

# Wait for the spider to finish
while (int(zap.spider.status()) < 100):
    print('Spider progress %: ' + zap.spider.status())
    time.sleep(2)

print('Spider completed')

# Start scanning
print('Scanning target %s' % target)
zap.ascan.scan(target)

# Wait for the scanner to finish
while (int(zap.ascan.status()) < 100):
    print('Scan progress %: ' + zap.ascan.status())
    time.sleep(5)

print('Scan completed')

# Report generation (HTML format)
print('Generating HTML report')
report_html = zap.core.htmlreport()

# Save report to file
with open('zap_report.html', 'w') as f:
    f.write(report_html)

print('HTML report saved to zap_report.html')

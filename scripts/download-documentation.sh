# Recursively download all linked pages
# Download all necessary files for offline viewing
# Save files with .html extension
# Convert to local links for offline viewing
# Restrict to the specified domain
# Do not ascend to parent directories
# Wait 2 seconds between requests to avoid overwhelming the server
# Add random wait to prevent bot detection
# Save files to the specified directory

wget \
  --recursive \
  --page-requisites \
  --html-extension \
  --convert-links \
  --domains rapidscada.net \
  --no-parent \
  --wait=2 \
  --random-wait \
  --directory-prefix=data/docs \
  'https://rapidscada.net/docs/en/latest/software-overview/' \
  'https://rapidscada.net/docs/en/latest/installation/' \
  'https://rapidscada.net/docs/en/latest/configuration/' \
  'https://rapidscada.net/docs/en/latest/modules/' \
  'https://rapidscada.net/docs/en/latest/additional-applications/' \
  'https://rapidscada.net/docs/en/latest/enterprise-edition/' \
  'https://rapidscada.net/docs/en/latest/developers/' \
  'https://rapidscada.net/docs/en/latest/version-history/'

# Troubleshooting

## Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `缺少必需的 Cookie` | cookies.json missing or invalid | Run `uv run gemini-web auth login` |
| `401 Unauthorized` | Cookie expired | Re-login to refresh cookies |
| `Image generation failed` | No permission or policy violation | Check account permissions, modify prompt |
| Authentication failure | Cookie expired | Run `uv run gemini-web auth login` |

## Cookie Refresh

If authentication fails:

```bash
uv run gemini-web auth login
```

Login to Google account and press Enter to retrieve new cookies.

## Automatic Cookie Refresh

The API automatically refreshes cookies by default. You may need to re-login occasionally - this is normal and won't affect functionality.

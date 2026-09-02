Subresource Integrity — SRI

Например:
<script
  src="https://cdn.example.com/app.js"
  integrity="sha256-..."
></script>

Браузер проверяет хэш загруженного ресурса.

Идея: «Я ожидал именно этот JavaScript. Если CDN отдаст другой — не выполняй его».
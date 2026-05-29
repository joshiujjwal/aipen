import { createApp } from "./app";

const PORT = process.env["PORT"] ?? 3001;

const app = createApp();
app.listen(PORT, () => {
  console.log(`API Gateway running on http://localhost:${PORT}`);
});

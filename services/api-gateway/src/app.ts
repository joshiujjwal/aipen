import express from "express";
import helmet from "helmet";
import cors from "cors";
import pinoHttp from "pino-http";
import { healthRouter } from "./routes/health";

export function createApp() {
  const app = express();

  // Middleware
  app.use(helmet());
  app.use(cors({ origin: process.env["CORS_ORIGIN"] ?? "http://localhost:5173" }));
  app.use(express.json());
  app.use(pinoHttp());

  // Routes
  app.use("/healthz", healthRouter);

  // TODO Phase 0: auth routes
  // TODO Phase 1: job routes
  // TODO Phase 1: notes routes
  // TODO Phase 4: WebSocket handler

  return app;
}

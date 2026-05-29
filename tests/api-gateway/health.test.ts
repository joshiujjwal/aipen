import request from "supertest";
import { createApp } from "../../src/app";

describe("GET /healthz", () => {
  const app = createApp();

  it("returns 200 with status ok", async () => {
    const res = await request(app).get("/healthz");
    expect(res.status).toBe(200);
    expect(res.body).toMatchObject({ status: "ok", service: "api-gateway" });
  });
});

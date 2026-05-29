import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import App from "../App";

// Smoke test — confirms app renders without crashing
describe("App", () => {
  it("renders without crashing", () => {
    render(<App />);
    // UploadPage is the default route
    expect(screen.getByText("AIPen")).toBeInTheDocument();
  });
});

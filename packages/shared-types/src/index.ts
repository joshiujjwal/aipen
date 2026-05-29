import { z } from "zod";

// ─── Enums ────────────────────────────────────────────────────────────────────

export const JobStatusSchema = z.enum(["pending", "processing", "done", "failed"]);
export type JobStatus = z.infer<typeof JobStatusSchema>;

export const InferenceEngineSchema = z.enum(["trocr", "tesseract"]);
export type InferenceEngine = z.infer<typeof InferenceEngineSchema>;

// ─── Handwriting Job ──────────────────────────────────────────────────────────

export const HandwritingJobSchema = z.object({
  id: z.string().uuid(),
  userId: z.string().uuid(),
  status: JobStatusSchema,
  imageUrl: z.string().url().optional(),
  engine: InferenceEngineSchema,
  createdAt: z.string().datetime(),
  updatedAt: z.string().datetime(),
});
export type HandwritingJob = z.infer<typeof HandwritingJobSchema>;

// ─── Recognition Result ───────────────────────────────────────────────────────

export const WordResultSchema = z.object({
  word: z.string(),
  confidence: z.number().min(0).max(1),
  bbox: z.tuple([z.number(), z.number(), z.number(), z.number()]), // x, y, w, h
});
export type WordResult = z.infer<typeof WordResultSchema>;

export const RecognitionResultSchema = z.object({
  jobId: z.string().uuid(),
  text: z.string(),
  words: z.array(WordResultSchema),
  engine: InferenceEngineSchema,
  modelVersion: z.string(),
  processingMs: z.number().int().nonnegative(),
});
export type RecognitionResult = z.infer<typeof RecognitionResultSchema>;

// ─── Notes ────────────────────────────────────────────────────────────────────

export const NoteSchema = z.object({
  id: z.string().uuid(),
  userId: z.string().uuid(),
  jobId: z.string().uuid(),
  title: z.string(),
  rawText: z.string(),
  wordData: z.array(WordResultSchema),
  imageUrl: z.string().url().optional(),
  createdAt: z.string().datetime(),
  updatedAt: z.string().datetime(),
});
export type Note = z.infer<typeof NoteSchema>;

// ─── Live Stroke Streaming ────────────────────────────────────────────────────

export const StrokeEventSchema = z.object({
  sessionId: z.string(),
  x: z.number(),
  y: z.number(),
  pressure: z.number().min(0).max(1),
  timestamp: z.number(), // unix ms
  isLiftOff: z.boolean(),
});
export type StrokeEvent = z.infer<typeof StrokeEventSchema>;

export const LiveInferenceChunkSchema = z.object({
  sessionId: z.string(),
  partialText: z.string(),
  isFinal: z.boolean(),
});
export type LiveInferenceChunk = z.infer<typeof LiveInferenceChunkSchema>;

// ─── API Request / Response ───────────────────────────────────────────────────

export const CreateJobRequestSchema = z.object({
  engine: InferenceEngineSchema.default("trocr"),
});
export type CreateJobRequest = z.infer<typeof CreateJobRequestSchema>;

export const PaginatedNotesSchema = z.object({
  items: z.array(NoteSchema),
  total: z.number().int().nonnegative(),
  page: z.number().int().positive(),
  perPage: z.number().int().positive(),
});
export type PaginatedNotes = z.infer<typeof PaginatedNotesSchema>;

export const RegisterRequestSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8).max(128),
});
export type RegisterRequest = z.infer<typeof RegisterRequestSchema>;

export const LoginRequestSchema = RegisterRequestSchema;
export type LoginRequest = RegisterRequest;

export const AuthTokensSchema = z.object({
  accessToken: z.string(),
  refreshToken: z.string(),
  expiresIn: z.number().int().positive(),
});
export type AuthTokens = z.infer<typeof AuthTokensSchema>;

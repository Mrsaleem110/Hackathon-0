export async function GET() {
  const stats = {
    platforms: 6,
    actions: 247,
    successRate: 87.4,
    uptime: 99.8,
  }

  return Response.json(stats)
}

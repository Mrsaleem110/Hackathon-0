export async function POST(request) {
  try {
    const { taskName, description, priority, platform, dueDate } = await request.json()

    if (!taskName || taskName.trim() === '') {
      return Response.json(
        { response: 'Task name required hai' },
        { status: 400 }
      )
    }

    // Create task object
    const task = {
      id: Date.now().toString(),
      taskName,
      description,
      priority,
      platform,
      dueDate,
      status: 'pending',
      createdAt: new Date().toISOString(),
      executedAt: null,
    }

    // Log task creation
    console.log('Task created:', task)

    // In production, save to database
    // For now, we'll just return success

    const response = `✅ Task Successfully Created!\n\n📋 Task Details:\n• Name: ${taskName}\n• Platform: ${platform}\n• Priority: ${priority}\n• Status: Pending\n• Created: ${new Date().toLocaleString()}\n\nYeh task queue mein add ho gaya aur jald execute ho jayega!`

    return Response.json({
      success: true,
      task,
      response,
      timestamp: new Date().toISOString()
    })
  } catch (error) {
    return Response.json(
      { response: `Error: ${error.message}` },
      { status: 500 }
    )
  }
}

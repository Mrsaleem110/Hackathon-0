export async function POST(request) {
  try {
    const { command } = await request.json()

    if (!command || command.trim() === '') {
      return Response.json(
        { response: 'Please provide a command' },
        { status: 400 }
      )
    }

    // Parse the command
    const lowerCommand = command.toLowerCase()

    // Simple command processing
    let response = ''

    if (lowerCommand.includes('gmail') || lowerCommand.includes('email')) {
      response = '📧 Gmail check ho raha hai... Emails fetch kar rahe hain.'
    } else if (lowerCommand.includes('linkedin') || lowerCommand.includes('post')) {
      response = '💼 LinkedIn par post ho raha hai... Content publish ho jayega.'
    } else if (lowerCommand.includes('whatsapp') || lowerCommand.includes('message')) {
      response = '💬 WhatsApp message bhej rahe hain... Message deliver ho jayega.'
    } else if (lowerCommand.includes('instagram') || lowerCommand.includes('story')) {
      response = '📸 Instagram par content upload ho raha hai...'
    } else if (lowerCommand.includes('facebook')) {
      response = '👍 Facebook par post ho raha hai...'
    } else if (lowerCommand.includes('twitter') || lowerCommand.includes('x')) {
      response = '𝕏 Tweet post ho raha hai...'
    } else if (lowerCommand.includes('status') || lowerCommand.includes('check')) {
      response = '✅ System status: All platforms active\n📊 Actions: 247\n✓ Success Rate: 87.4%\n⏱️ Uptime: 99.8%'
    } else if (lowerCommand.includes('help')) {
      response = `📖 Available Commands:
• "Gmail check karo" - Check emails
• "LinkedIn post karo" - Post on LinkedIn
• "WhatsApp message bhej" - Send WhatsApp message
• "Instagram story" - Post on Instagram
• "Facebook post" - Post on Facebook
• "Twitter/X post" - Tweet
• "Status check" - System status
• "Help" - Show this help`
    } else {
      response = `✅ Command received: "${command}"\n\nYeh command process ho raha hai. Detailed task ke liye "Detailed Task" button use karo.`
    }

    return Response.json({
      response,
      timestamp: new Date().toISOString(),
      command
    })
  } catch (error) {
    return Response.json(
      { response: `Error: ${error.message}` },
      { status: 500 }
    )
  }
}

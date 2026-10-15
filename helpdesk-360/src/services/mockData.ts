import type { Ticket, Message, AiAnalysis, AiAssist, Status, Priority, Role } from '../types'

const SEED_TICKETS: Ticket[] = [
  {
    id: 'HD-101',
    title: 'VPN connection dropping repeatedly during remote work',
    description: 'My Cisco AnyConnect VPN client disconnects every 10-15 minutes while connected to the European gateway, interrupting Docker pushes and active SSH sessions.',
    status: 'In Progress',
    priority: 'High',
    category: 'Network',
    employee: 'Sarah Connor',
    department: 'Engineering',
    device: 'MacBook Pro 16" (M2 Max)',
    updatedAt: new Date(Date.now() - 1000 * 60 * 35).toISOString(),
    slaDueAt: new Date(Date.now() + 1000 * 60 * 135).toISOString(),
  },
  {
    id: 'HD-102',
    title: 'Request temporary IAM access to AWS production EKS cluster',
    description: 'Need read-only kubectl access to the production EKS cluster to verify pod rollout metrics for the v2.4 deployment.',
    status: 'New',
    priority: 'Critical',
    category: 'Access',
    employee: 'Alex Mercer',
    department: 'DevOps',
    device: 'ThinkPad X1 Carbon Gen 10',
    updatedAt: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
    slaDueAt: new Date(Date.now() + 1000 * 60 * 45).toISOString(),
  },
  {
    id: 'HD-103',
    title: 'Figma desktop app crashes on startup with memory fault',
    description: 'After the latest macOS update, launching the Figma app results in an immediate crash report citing EXC_BAD_ACCESS in the GPU rendering pipeline.',
    status: 'Assigned',
    priority: 'Medium',
    category: 'Software',
    employee: 'Emily Blunt',
    department: 'Product Design',
    device: 'Dell XPS 15 9520',
    updatedAt: new Date(Date.now() - 1000 * 60 * 140).toISOString(),
    slaDueAt: new Date(Date.now() + 1000 * 60 * 420).toISOString(),
  },
  {
    id: 'HD-104',
    title: 'External dual monitors not detected via Thunderbolt dock',
    description: 'Both 4K Dell monitors display "No DisplayPort Signal" when connected to the CalDigit TS4 dock, despite laptop charging normally.',
    status: 'Waiting for Employee',
    priority: 'Low',
    category: 'Hardware',
    employee: 'John Wick',
    department: 'Operations',
    device: 'HP EliteBook 840 G9',
    updatedAt: new Date(Date.now() - 1000 * 60 * 60 * 18).toISOString(),
    slaDueAt: new Date(Date.now() + 1000 * 60 * 60 * 8).toISOString(),
  },
  {
    id: 'HD-105',
    title: 'Slack push notifications delayed on mobile client',
    description: 'Direct mentions and urgent huddle alerts are not vibrating or appearing on the lock screen until the Slack app is manually opened.',
    status: 'Resolved',
    priority: 'Medium',
    category: 'Software',
    employee: 'Claire Redfield',
    department: 'Marketing',
    device: 'iPhone 15 Pro (iOS 18)',
    updatedAt: new Date(Date.now() - 1000 * 60 * 60 * 6).toISOString(),
    slaDueAt: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(),
  },
  {
    id: 'HD-106',
    title: 'Replace degraded laptop battery (Service Recommended)',
    description: 'Battery health has dropped to 62% maximum capacity. Machine shuts down unexpectedly when unplugged from AC adapter.',
    status: 'Closed',
    priority: 'Low',
    category: 'Hardware',
    employee: 'Bruce Wayne',
    department: 'Executive',
    device: 'MacBook Air M2',
    updatedAt: new Date(Date.now() - 1000 * 60 * 60 * 48).toISOString(),
    slaDueAt: new Date(Date.now() - 1000 * 60 * 60 * 30).toISOString(),
  },
]

const SEED_MESSAGES: Record<string, Message[]> = {
  'HD-101': [
    {
      id: 'm-101-1',
      author: 'Sarah Connor',
      kind: 'employee',
      body: 'My Cisco AnyConnect VPN client disconnects every 10-15 minutes while connected to the European gateway, interrupting Docker pushes and active SSH sessions.',
      createdAt: new Date(Date.now() - 1000 * 60 * 90).toISOString(),
    },
    {
      id: 'm-101-2',
      author: 'Dev Technician',
      kind: 'technician',
      body: 'Hi Sarah, this is typically due to an MTU size mismatch on local ISP connections or AnyConnect auto-reconnect timeouts. Could you try setting your interface MTU to 1350?',
      createdAt: new Date(Date.now() - 1000 * 60 * 45).toISOString(),
    },
    {
      id: 'm-101-3',
      author: 'Dev Technician',
      kind: 'internal',
      body: 'Confirmed multiple engineers on Comcast residential gateways experienced AnyConnect keepalive dropouts today. Working on a group policy push.',
      createdAt: new Date(Date.now() - 1000 * 60 * 40).toISOString(),
    },
  ],
  'HD-102': [
    {
      id: 'm-102-1',
      author: 'Alex Mercer',
      kind: 'employee',
      body: 'Need read-only kubectl access to the production EKS cluster to verify pod rollout metrics for the v2.4 deployment.',
      createdAt: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
    },
  ],
  'HD-103': [
    {
      id: 'm-103-1',
      author: 'Emily Blunt',
      kind: 'employee',
      body: 'After the latest macOS update, launching the Figma app results in an immediate crash report citing EXC_BAD_ACCESS in the GPU rendering pipeline.',
      createdAt: new Date(Date.now() - 1000 * 60 * 140).toISOString(),
    },
  ],
  'HD-104': [
    {
      id: 'm-104-1',
      author: 'John Wick',
      kind: 'employee',
      body: 'Both 4K Dell monitors display "No DisplayPort Signal" when connected to the CalDigit TS4 dock, despite laptop charging normally.',
      createdAt: new Date(Date.now() - 1000 * 60 * 60 * 18).toISOString(),
    },
    {
      id: 'm-104-2',
      author: 'IT Support',
      kind: 'technician',
      body: 'Please disconnect power to the CalDigit dock for 30 seconds to discharge residual power, and verify Thunderbolt security authorization in Windows Settings.',
      createdAt: new Date(Date.now() - 1000 * 60 * 60 * 10).toISOString(),
    },
  ],
}

const KB_ARTICLES = [
  {
    id: 'kb-1',
    title: 'How to Connect to Corporate VPN & Troubleshoot Drops',
    category: 'Network',
    steps: [
      'Open Cisco AnyConnect client from Applications or System Tray.',
      'Enter gateway address: vpn.company.com and select your regional server.',
      'Authenticate with your corporate email and approve the Duo/Okta push notification.',
      'If frequent disconnects occur, lower your MTU to 1350 via Terminal: "sudo ifconfig en0 mtu 1350".',
      'Disable third-party DNS or VPN clients (e.g. Cloudflare WARP) before reconnecting.',
    ],
  },
  {
    id: 'kb-2',
    title: 'Requesting Temporary Access & Cloud Permissions',
    category: 'Access',
    steps: [
      'Navigate to the internal Access Management Portal (access.company.internal).',
      'Select the target environment (e.g. AWS Production EKS, Snowflake, GitHub Admin).',
      'Enter business justification and manager approval reference.',
      'Temporary credentials expire automatically after 8 hours.',
    ],
  },
  {
    id: 'kb-3',
    title: 'Resolving Dual External Monitors & Docking Station Issues',
    category: 'Hardware',
    steps: [
      'Unplug the Thunderbolt/USB-C host cable from your laptop.',
      'Disconnect power from the dock for 30 seconds, then reconnect power.',
      'Ensure both DisplayPort/HDMI cables are firmly seated in the monitor ports.',
      'Plug the host cable back into your laptop and check OS Display Settings.',
      'For Mac users, ensure "Allow accessories to connect" is set to "Automatically".',
    ],
  },
  {
    id: 'kb-4',
    title: 'Self-Service Software Installation & License Activation',
    category: 'Software',
    steps: [
      'Launch the Company Portal (Windows) or Jamf Self Service (macOS).',
      'Browse approved developer and design software (Docker, Figma, IntelliJ, Postman).',
      'Click Install; admin credentials are not required for catalog software.',
      'If license key required, visit licenses.company.internal for automated SSO allocation.',
    ],
  },
  {
    id: 'kb-5',
    title: 'Multi-Factor Authentication (MFA) Reset Procedure',
    category: 'Access',
    steps: [
      'If you lost access to your primary authenticator device, visit auth.company.com/recover.',
      'Authenticate using your secondary emergency SMS backup number or printed emergency kit code.',
      'Register your new device by scanning the generated QR code.',
      'Contact the IT Service Desk if emergency backup codes are unavailable.',
    ],
  },
]

function getStoredTickets(): Ticket[] {
  try {
    const raw = localStorage.getItem('helpdesk_mock_tickets')
    if (raw) return JSON.parse(raw)
  } catch {
    // fallback
  }
  return SEED_TICKETS
}

function saveStoredTickets(tickets: Ticket[]) {
  try {
    localStorage.setItem('helpdesk_mock_tickets', JSON.stringify(tickets))
  } catch {
    // ignore
  }
}

function getStoredMessages(): Record<string, Message[]> {
  try {
    const raw = localStorage.getItem('helpdesk_mock_messages')
    if (raw) return JSON.parse(raw)
  } catch {
    // fallback
  }
  return SEED_MESSAGES
}

function saveStoredMessages(messages: Record<string, Message[]>) {
  try {
    localStorage.setItem('helpdesk_mock_messages', JSON.stringify(messages))
  } catch {
    // ignore
  }
}

export const mockDb = {
  getTickets: (params?: { q?: string; status?: string }): Ticket[] => {
    let list = getStoredTickets()
    if (params?.status) {
      list = list.filter(t => t.status === params.status)
    }
    if (params?.q) {
      const q = params.q.toLowerCase()
      list = list.filter(t => t.title.toLowerCase().includes(q) || t.description.toLowerCase().includes(q))
    }
    return list
  },

  getTicket: (id: string): Ticket => {
    const list = getStoredTickets()
    const ticket = list.find(t => t.id === id)
    if (!ticket) {
      throw new Error(`Ticket ${id} not found`)
    }
    return ticket
  },

  createTicket: (data: FormData | Record<string, any>): Ticket => {
    const list = getStoredTickets()
    const messages = getStoredMessages()
    
    let title = ''
    let description = ''
    let category = 'Other'
    let priority: Priority = 'Medium'
    let department = 'General'
    let device = 'Workstation'

    if (data instanceof FormData) {
      title = (data.get('title') as string) || 'Untitled ticket'
      description = (data.get('description') as string) || ''
      category = (data.get('category') as string) || 'Other'
      priority = ((data.get('priority') as string) || 'Medium') as Priority
      department = (data.get('department') as string) || 'General'
      device = (data.get('device') as string) || 'Workstation'
    } else {
      title = data.title || 'Untitled ticket'
      description = data.description || ''
      category = data.category || 'Other'
      priority = data.priority || 'Medium'
      department = data.department || 'General'
      device = data.device || 'Workstation'
    }

    const nextId = `HD-${100 + list.length + 1}`
    const now = new Date().toISOString()
    const slaDueAt = new Date(Date.now() + 1000 * 60 * 60 * (priority === 'Critical' ? 4 : priority === 'High' ? 8 : 24)).toISOString()

    const newTicket: Ticket = {
      id: nextId,
      title,
      description,
      status: 'New',
      priority,
      category,
      employee: 'Sarah Connor',
      department,
      device,
      updatedAt: now,
      slaDueAt,
    }

    const updatedList = [newTicket, ...list]
    saveStoredTickets(updatedList)

    messages[nextId] = [
      {
        id: `m-${nextId}-1`,
        author: 'Sarah Connor',
        kind: 'employee',
        body: description,
        createdAt: now,
      },
    ]
    saveStoredMessages(messages)

    return newTicket
  },

  setStatus: (id: string, status: Status): Ticket => {
    const list = getStoredTickets()
    const idx = list.findIndex(t => t.id === id)
    if (idx === -1) throw new Error(`Ticket ${id} not found`)
    
    list[idx] = {
      ...list[idx],
      status,
      updatedAt: new Date().toISOString(),
    }
    saveStoredTickets(list)
    return list[idx]
  },

  getMessages: (ticketId: string): Message[] => {
    const messages = getStoredMessages()
    if (messages[ticketId]) return messages[ticketId]

    // Provide default initial message if none exists
    const ticket = getStoredTickets().find(t => t.id === ticketId)
    if (ticket) {
      return [
        {
          id: `m-${ticketId}-init`,
          author: ticket.employee || 'Employee',
          kind: 'employee',
          body: ticket.description,
          createdAt: ticket.updatedAt,
        },
      ]
    }
    return []
  },

  reply: (ticketId: string, body: string, kind: Message['kind']): Message => {
    const messages = getStoredMessages()
    const list = getStoredTickets()
    const now = new Date().toISOString()

    const newMessage: Message = {
      id: `m-${ticketId}-${Date.now()}`,
      author: kind === 'employee' ? 'Sarah Connor' : 'Dev Technician',
      kind,
      body,
      createdAt: now,
    }

    messages[ticketId] = [...(messages[ticketId] || []), newMessage]
    saveStoredMessages(messages)

    const tIdx = list.findIndex(t => t.id === ticketId)
    if (tIdx !== -1) {
      list[tIdx].updatedAt = now
      saveStoredTickets(list)
    }

    return newMessage
  },

  analyze: (text: string): AiAnalysis => {
    const lower = text.toLowerCase()
    let category = 'Software'
    let priority: Priority = 'Medium'
    let summary = 'Standard employee support request requiring technician triage.'

    if (/(vpn|wifi|wi-fi|network|internet|dns|gateway|packet|ethernet|slow connection)/.test(lower)) {
      category = 'Network'
      priority = /(down|disconnected|critical|cannot work|dropping)/.test(lower) ? 'High' : 'Medium'
      summary = 'Network connectivity / VPN instability detected. Client-side adapter or gateway routing may need adjustments.'
    } else if (/(access|permission|password|login|auth|iam|aws|token|mfa|account)/.test(lower)) {
      category = 'Access'
      priority = /(production|prod|urgent|blocked|critical)/.test(lower) ? 'Critical' : 'High'
      summary = 'Credentials or elevated permission request. Verification of authorization policies required.'
    } else if (/(monitor|screen|dock|laptop|battery|charger|keyboard|mouse|hardware|macbook|dell|cable)/.test(lower)) {
      category = 'Hardware'
      priority = /(battery|shut down|fire|damage|broken)/.test(lower) ? 'High' : 'Low'
      summary = 'Physical peripheral or hardware diagnostic required. Check firmware drivers or schedule device replacement.'
    } else if (/(crash|crashes|bug|error|freeze|frozen|slack|figma|install|app)/.test(lower)) {
      category = 'Software'
      priority = /(crash|freeze|blocking)/.test(lower) ? 'Medium' : 'Low'
      summary = 'Software application execution error or dependency crash. Cache clearing or reinstallation recommended.'
    }

    return { category, priority, summary }
  },

  assist: (ticketId: string): AiAssist => {
    const ticket = mockDb.getTicket(ticketId)
    const cat = ticket.category

    if (cat === 'Network') {
      return {
        summary: `Network connection disruptions reported by ${ticket.employee || 'employee'}. Likely MTU packet mismatch or VPN profile certificate renewal.`,
        solution: 'Adjust local network MTU to 1350, flush DNS caches, and ensure Cisco AnyConnect profile is updated to v4.10+.',
        draftReply: `Hello ${ticket.employee ? ticket.employee.split(' ')[0] : 'there'},\n\nWe looked into the VPN disconnection issue you reported. This is frequently related to packet fragmentation on residential ISPs. Could you please run the following command to set your MTU size to 1350 and re-test?\n\n$ sudo ifconfig en0 mtu 1350\n\nPlease let us know if the connection stabilizes.`,
        steps: [
          'Verify gateway reachability via ping vpn.company.com',
          'Inspect client AnyConnect diagnostics log (DART report)',
          'Adjust MTU packet size to 1350 or 1400',
          'Verify split-tunnel IP routing rules',
        ],
        articles: [
          { id: 'kb-1', title: 'How to Connect to Corporate VPN & Troubleshoot Drops' },
        ],
      }
    } else if (cat === 'Access') {
      return {
        summary: `IAM elevated access request for ${ticket.department || 'user'} team. Verification of role assignment and temporary credentials expiry required.`,
        solution: 'Provision short-lived IAM role session with AWS STS or Okta SSO group membership and 8-hour TTL.',
        draftReply: `Hello ${ticket.employee ? ticket.employee.split(' ')[0] : 'there'},\n\nYour temporary access request for ${ticket.title} has been received. Please verify that your manager has approved the request in the Access Management Portal so we can issue your session credentials.`,
        steps: [
          'Verify requester identity and manager sign-off',
          'Generate temporary IAM role credentials via STS AssumeRole',
          'Send session config instructions to user securely',
        ],
        articles: [
          { id: 'kb-2', title: 'Requesting Temporary Access & Cloud Permissions' },
          { id: 'kb-5', title: 'Multi-Factor Authentication (MFA) Reset Procedure' },
        ],
      }
    } else if (cat === 'Hardware') {
      return {
        summary: `Hardware fault reported on device ${ticket.device || 'workstation'}. Hardware reset or warranty repair needed.`,
        solution: 'Perform power cycle reset on external peripherals, verify Thunderbolt security policies, or issue replacement unit from IT locker.',
        draftReply: `Hi ${ticket.employee ? ticket.employee.split(' ')[0] : 'there'},\n\nThanks for reaching out. We have logged this hardware ticket for your ${ticket.device || 'device'}. Please try disconnecting power for 30 seconds to drain capacitors. If the issue persists, we can swap the unit at the IT desk.`,
        steps: [
          'Power cycle dock/monitor hardware',
          'Check device manager for driver warning badges',
          'Test with certified Thunderbolt 4 replacement cable',
          'Schedule hardware swap if diagnostic fails',
        ],
        articles: [
          { id: 'kb-3', title: 'Resolving Dual External Monitors & Docking Station Issues' },
        ],
      }
    } else {
      return {
        summary: `Application issue regarding ${ticket.title}. Investigating application logs and OS compatibility.`,
        solution: 'Clear application local storage / cache directories and verify latest patch installation from Self Service.',
        draftReply: `Hello ${ticket.employee ? ticket.employee.split(' ')[0] : 'there'},\n\nWe reviewed your ticket regarding ${ticket.title}. Please check whether the app has pending updates in Self Service Portal, or try clearing the local cache directory.`,
        steps: [
          'Review crash logs and stack trace',
          'Clear app application support / cache directory',
          'Reinstall latest certified build from Company Portal',
        ],
        articles: [
          { id: 'kb-4', title: 'Self-Service Software Installation & License Activation' },
        ],
      }
    }
  },

  chat: (message: string): { reply: string } => {
    const q = message.toLowerCase()
    if (/(wifi|wi-fi|internet|network|slow|vpn)/.test(q)) {
      return {
        reply: 'For WiFi and VPN issues: 1) Ensure you are connected to "Company-Secure" network. 2) In Cisco AnyConnect, connect to vpn.company.com. 3) If disconnections occur frequently, try lowering MTU to 1350. You can also view our knowledge base article "How to Connect to Corporate VPN".',
      }
    }
    if (/(password|reset|forgot|login|access|mfa)/.test(q)) {
      return {
        reply: 'To reset your password or MFA token, visit auth.company.com/recover from an approved browser, or submit an "Access" ticket and our IT team will assist with identity verification.',
      }
    }
    if (/(monitor|screen|dock|display|hdmi)/.test(q)) {
      return {
        reply: 'For monitor or dock problems: Unplug the host USB-C/Thunderbolt cable, power down the dock for 30 seconds, plug it back in, and ensure OS Display Settings has detected the second display.',
      }
    }
    if (/(laptop|battery|hardware|mouse|keyboard)/.test(q)) {
      return {
        reply: 'If your laptop battery is degraded or peripherals are malfunctioning, you can create a ticket with category "Hardware". We can arrange an on-site inspection or IT locker replacement.',
      }
    }
    return {
      reply: 'I am your HelpDesk-360 AI assistant. I can help troubleshoot network issues, software crashes, access requests, and hardware setups. How can I assist you today?',
    }
  },

  searchKb: (q?: string) => {
    if (!q || !q.trim()) return KB_ARTICLES
    const query = q.toLowerCase()
    return KB_ARTICLES.filter(
      a =>
        a.title.toLowerCase().includes(query) ||
        a.category.toLowerCase().includes(query) ||
        a.steps.some(s => s.toLowerCase().includes(query))
    )
  },

  getActivity: () => [
    {
      id: 'act-1',
      text: 'Ticket HD-102 assigned to Critical Incident Triage',
      at: new Date(Date.now() - 1000 * 60 * 12).toISOString(),
    },
    {
      id: 'act-2',
      text: 'Technician replied to HD-101 (VPN instability)',
      at: new Date(Date.now() - 1000 * 60 * 45).toISOString(),
    },
    {
      id: 'act-3',
      text: 'Ticket HD-105 marked as Resolved',
      at: new Date(Date.now() - 1000 * 60 * 60 * 6).toISOString(),
    },
    {
      id: 'act-4',
      text: 'Knowledge base article "Corporate VPN Setup" updated',
      at: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(),
    },
  ],

  getAnalytics: () => ({
    volume: [
      { day: 'Mon', count: 18 },
      { day: 'Tue', count: 24 },
      { day: 'Wed', count: 19 },
      { day: 'Thu', count: 31 },
      { day: 'Fri', count: 22 },
      { day: 'Sat', count: 7 },
      { day: 'Sun', count: 5 },
    ],
    categories: [
      { name: 'Network', value: 38 },
      { name: 'Software', value: 45 },
      { name: 'Hardware', value: 28 },
      { name: 'Access', value: 20 },
      { name: 'Other', value: 9 },
    ],
    workload: [
      { name: 'Alex M.', open: 4, solved: 21 },
      { name: 'Jordan K.', open: 7, solved: 26 },
      { name: 'Sam T.', open: 3, solved: 18 },
      { name: 'Taylor R.', open: 5, solved: 15 },
    ],
    avgResolutionHours: 3.4,
  }),

  getNotifications: () => [
    { id: 'notif-1', text: 'Critical ticket HD-102 SLA expires in 30 minutes' },
    { id: 'notif-2', text: 'Sarah Connor updated ticket HD-101' },
  ],

  login: (email: string, _password: string) => {
    const role: Role = email.includes('tech') ? 'technician' : 'employee'
    const name = email.split('@')[0].replace(/[._-]/g, ' ')
    const formattedName = name.charAt(0).toUpperCase() + name.slice(1)
    return {
      token: 'dev',
      user: {
        id: 'user-dev',
        name: formattedName || 'Demo User',
        email,
        role,
      },
    }
  },
}

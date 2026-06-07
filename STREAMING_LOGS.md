# Real-Time Streaming Logs Feature

## Overview

The AI Research Assistant now features **enhanced real-time streaming logs** that provide detailed progress updates during the research process. This gives users complete visibility into what each agent is doing at every step.

## Features

### ✨ Real-Time Updates
- **Live streaming** via Server-Sent Events (SSE)
- **Instant feedback** as each agent processes data
- **No waiting** - see progress as it happens

### 🕐 Timestamps
- Every log entry includes a precise timestamp `[HH:MM:SS]`
- Helps track performance and identify bottlenecks
- Example: `[16:21:45] 🚀 Starting research on: "Neural Networks"`

### 🎨 Color-Coded Log Levels
Logs are categorized by severity and colored accordingly:

| Level | Color | Usage |
|-------|-------|-------|
| `info` | 🔵 Blue | General progress updates |
| `success` | 🟢 Green | Completed tasks, milestones |
| `warning` | 🟡 Yellow | Non-critical issues |
| `error` | 🔴 Red | Critical errors, failures |

### 📊 Detailed Progress Information

#### Planner Agent
```
[16:21:46] 🧠 Planner Agent: Breaking down research topic into sections...
[16:21:46] ✅ Planner Agent: Generated 7 research sections
[16:21:46]    📋 Section 1: Introduction to Neural Networks
[16:21:46]    📋 Section 2: Types of Neural Networks
...
```

#### Research Agent
```
[16:21:47] 🔍 Research Agent: Starting web research for 7 sections...
[16:21:52] ✅ Research Agent: Completed web research for 7 sections
```

#### Paper Analyzer
```
[16:21:52] 📖 Paper Analyzer: Searching arXiv for academic papers...
[16:22:07] ✅ Paper Analyzer: Found 35 academic papers across 7 sections
```

#### Insight Extractor
```
[16:22:07] ✨ Insight Extractor: Extracting key research insights from papers...
[16:22:12] ✅ Insight Extractor: Extracted insights from 7 sections
```

#### Source Ranker
```
[16:22:13] 🔧 Source Ranker: Evaluating and ranking sources by quality...
[16:22:14] ✅ Source Ranker: Ranked and filtered 7 sections by quality
```

#### Critic Agent
```
[16:22:15] 🛡️ Critic Agent: Validating and refining research data...
[16:22:18] ✅ Critic Agent: Validated and refined 7 sections
```

#### Writer Agent
```
[16:22:18] ✍️ Writer Agent: Generating comprehensive research report...
[16:22:20] ✅ Writer Agent: Generated report with ~481 words
```

#### Citation Agent
```
[16:22:20] 💬 Citation Agent: Adding inline citations and references...
[16:22:23] ✅ Citation Agent: Added 20 unique citations to report
```

### 🎬 Smooth Animations
- **Typing effect**: Logs appear with smooth fade-in animations
- **Auto-scroll**: Logs container automatically scrolls to show latest entries
- **Hover effects**: Interactive hover states for better UX

### 📱 Responsive Design
- Works seamlessly on desktop and mobile
- Sticky agent panel stays visible while scrolling
- Optimized log container height (max 96 units)

## Technical Implementation

### Backend (FastAPI + SSE)

**File**: `backend/api.py`

```python
from datetime import datetime

def get_timestamp():
    """Get formatted timestamp for logs"""
    return datetime.now().strftime("%H:%M:%S")

async def send_log(message: str, level: str = "info"):
    """Helper to format and send log messages with timestamps"""
    timestamp = get_timestamp()
    log_data = {
        'type': 'log',
        'message': message,
        'timestamp': timestamp,
        'level': level  # info, success, warning, error
    }
    return f"data: {json.dumps(log_data)}\n\n"
```

**Log Examples**:
```python
# Info log
yield await send_log('🧠 Planner Agent: Breaking down research topic...', 'info')

# Success log
yield await send_log(f'✅ Planner Agent: Generated {len(sections)} research sections', 'success')

# Error log
yield await send_log(f'❌ Error: {str(e)}', 'error')
```

### Frontend (Next.js + React)

**File**: `frontend/app/page.tsx`

**Log Entry Interface**:
```typescript
interface LogEntry {
  message: string;
  timestamp: string;
  level: string; // info, success, warning, error
}
```

**Color Coding**:
```typescript
const logColors: Record<string, string> = {
  info: "text-blue-300 border-blue-500/30",
  success: "text-green-300 border-green-500/30",
  warning: "text-yellow-300 border-yellow-500/30",
  error: "text-red-300 border-red-500/30",
};
```

**Auto-Scroll Implementation**:
```typescript
const logsEndRef = useRef<HTMLDivElement>(null);

useEffect(() => {
  if (logsEndRef.current) {
    logsEndRef.current.scrollIntoView({ behavior: "smooth" });
  }
}, [logs]);
```

**Log Rendering with Animations**:
```typescript
<AnimatePresence mode="popLayout">
  {logs.map((log, index) => (
    <motion.div
      key={index}
      initial={{ opacity: 0, x: -10, height: 0 }}
      animate={{ opacity: 1, x: 0, height: "auto" }}
      transition={{ 
        duration: 0.3,
        delay: index * 0.02 
      }}
      className={`${logColors[log.level]} ...`}
    >
      <span className="text-gray-500 text-xs">
        [{log.timestamp}]
      </span>
      <span>{log.message}</span>
    </motion.div>
  ))}
</AnimatePresence>
```

## SSE Event Types

The backend sends three types of events:

### 1. Log Event
```json
{
  "type": "log",
  "message": "🚀 Starting research on: \"Neural Networks\"",
  "timestamp": "16:21:45",
  "level": "info"
}
```

### 2. Agent Status Event
```json
{
  "type": "agent_status",
  "agent": "planner",
  "status": "running"  // idle | running | completed
}
```

### 3. Final Report Event
```json
{
  "type": "final_report",
  "report": "# Neural Networks\n\n..."
}
```

## Performance Metrics

From test run with query "Neural Networks":

| Metric | Value |
|--------|-------|
| Total log entries | 25 |
| Agent status updates | 16 |
| Sections generated | 7 |
| Papers found | 35 |
| Citations added | 20 |
| Total time | ~38 seconds |
| Final report size | 5,701 characters |

## Testing

Run the test script to verify streaming logs:

```bash
cd backend
python test_streaming_logs.py
```

Expected output:
- ✓ Colored terminal output with timestamps
- ✓ Real-time progress updates for all 8 agents
- ✓ Summary statistics at the end

## Browser Usage

1. Open http://localhost:3000
2. Enter a research topic (e.g., "Deep Learning")
3. Click the send button
4. Watch the **Live Activity Logs** panel:
   - Timestamps appear on the left
   - Color-coded messages show progress
   - Container auto-scrolls to latest logs
   - Agent status panel updates in real-time

## Benefits

### For Users
- **Transparency**: See exactly what's happening at each step
- **Progress tracking**: Know how long each agent takes
- **Debugging**: Identify bottlenecks or issues quickly
- **Engagement**: Dynamic UI keeps users informed and engaged

### For Developers
- **Debugging**: Detailed logs help diagnose issues
- **Performance monitoring**: Timestamps reveal slow agents
- **Error tracking**: Color-coded errors are easy to spot
- **Testing**: Clear visibility into system behavior

## Future Enhancements

Potential improvements:
- [ ] Export logs to file
- [ ] Filter logs by level (info/success/error)
- [ ] Search/filter logs by keyword
- [ ] Pause/resume auto-scroll
- [ ] Collapsible agent sections
- [ ] Download logs as JSON/CSV
- [ ] Real-time performance graphs

## Related Files

- `backend/api.py` - SSE streaming implementation
- `frontend/app/page.tsx` - Frontend log display
- `frontend/app/globals.css` - Scrollbar and markdown styling
- `backend/test_streaming_logs.py` - Test script

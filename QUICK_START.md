# Quick Start Guide - Enhanced Streaming Logs

## 🚀 Get Started in 3 Minutes

### Step 1: Start the Servers

Open two terminals:

**Terminal 1 - Backend:**
```bash
cd "Research assisstant/backend"
python api.py
```

Wait for:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Terminal 2 - Frontend:**
```bash
cd "Research assisstant/frontend"
npm run dev
```

Wait for:
```
✓ Ready in 925ms
- Local:   http://localhost:3000
```

### Step 2: Open the Application

Open your browser and go to: **http://localhost:3000**

### Step 3: Try a Research Query

Enter one of these topics:
- "Neural Networks"
- "Quantum Computing"
- "Climate Change Solutions"
- "Artificial General Intelligence"

Click the send button (or press Enter).

## 🎯 What You'll See

### 1. Agent Pipeline Panel (Left Side)

Watch agents light up in sequence:

```
┌─────────────────────────────────┐
│ ✨ Agent Pipeline               │
│                                  │
│ ✓ 🧠 Planner        [Green]     │  ← Completed
│ ⟳ 🔍 Researcher     [Blue]      │  ← Currently Running
│   📖 Paper Analyzer [Gray]      │  ← Waiting
│   ✨ Insight Extractor [Gray]   │
│   🔧 Source Ranker  [Gray]      │
│   🛡️ Critic         [Gray]      │
│   ✍️ Writer         [Gray]      │
│   💬 Citation Agent [Gray]      │
└─────────────────────────────────┘
```

### 2. Live Activity Logs (Right Side)

Real-time logs with timestamps and colors:

```
┌──────────────────────────────────────────────────────────┐
│ 🕐 Live Activity Logs                                    │
│                                                           │
│ [16:21:45] 🚀 Starting research on: "Neural Networks"   │  ← Blue
│ [16:21:46] 🧠 Planner Agent: Breaking down research...  │  ← Blue
│ [16:21:46] ✅ Planner Agent: Generated 7 sections       │  ← Green
│ [16:21:46]    📋 Section 1: Introduction to NNs        │  ← Blue
│ [16:21:46]    📋 Section 2: Types of NNs               │  ← Blue
│ [16:21:47]    📋 Section 3: NN Architecture            │  ← Blue
│ [16:21:47] 🔍 Research Agent: Starting web research... │  ← Blue
│ [16:21:52] ✅ Research Agent: Completed for 7 sections │  ← Green
│ [16:21:52] 📖 Paper Analyzer: Searching arXiv...       │  ← Blue
│ [16:22:07] ✅ Paper Analyzer: Found 35 papers          │  ← Green
│ [16:22:07] ✨ Insight Extractor: Extracting insights...│  ← Blue
│ [16:22:12] ✅ Insight Extractor: Extracted from 7 sections│← Green
│ [16:22:13] 🔧 Source Ranker: Evaluating sources...     │  ← Blue
│ [16:22:14] ✅ Source Ranker: Ranked 7 sections         │  ← Green
│ [16:22:15] 🛡️ Critic Agent: Validating research...     │  ← Blue
│ [16:22:18] ✅ Critic Agent: Validated 7 sections       │  ← Green
│ [16:22:18] ✍️ Writer Agent: Generating report...       │  ← Blue
│ [16:22:20] ✅ Writer Agent: Generated report (~481 words)│← Green
│ [16:22:20] 💬 Citation Agent: Adding citations...      │  ← Blue
│ [16:22:23] ✅ Citation Agent: Added 20 citations       │  ← Green
│ [16:22:23] 🎉 Research completed successfully!         │  ← Green
│                                                           │
└──────────────────────────────────────────────────────────┘
    ↑ Auto-scrolls to show latest logs
```

### 3. Research Report (Bottom)

After completion, the report appears below:

```
┌──────────────────────────────────────────────────────────┐
│ 📄 Research Report                                       │
│                                                           │
│ # Neural Networks                                        │
│                                                           │
│ Neural networks are computational models inspired by     │
│ biological neurons [1], [2]. Recent advances have...    │
│                                                           │
│ ## Key Findings                                          │
│ - Deep learning architectures [3]                        │
│ - Training optimization techniques [4]                   │
│                                                           │
│ ## References                                            │
│ [1] Introduction to Neural Networks                      │
│ https://arxiv.org/pdf/...                               │
│                                                           │
│ [2] Deep Learning Fundamentals                           │
│ https://arxiv.org/pdf/...                               │
└──────────────────────────────────────────────────────────┘
```

## 🎨 Color Guide

| Color | Meaning | Example |
|-------|---------|---------|
| 🔵 **Blue** | Agent working | `[16:21:45] 🧠 Planner Agent: Breaking down...` |
| 🟢 **Green** | Task completed | `[16:21:46] ✅ Planner Agent: Generated 7 sections` |
| 🟡 **Yellow** | Warning | `[16:22:10] ⚠️ Only 3 papers found for this section` |
| 🔴 **Red** | Error | `[16:22:20] ❌ Error: Failed to fetch paper` |

## ⏱️ Expected Timeline

For a typical research query:

| Time | Event |
|------|-------|
| 0s | Query submitted |
| 1s | Planner completes (7 sections generated) |
| 6s | Researcher completes (parallel web searches) |
| 21s | Paper Analyzer completes (35 papers found) |
| 26s | Insight Extractor completes |
| 27s | Source Ranker completes |
| 30s | Critic Agent completes |
| 32s | Writer completes (report generated) |
| 35s | Citation Agent completes (citations added) |
| **~35-40s** | **Total time** |

## 🎯 What to Look For

### Smooth Animations
- Logs fade in smoothly (not instant)
- Each log appears with a slight delay
- Auto-scroll is smooth, not jumpy

### Real-Time Updates
- No waiting for all agents to finish
- See progress as it happens
- Timestamps show exact timing

### Detailed Information
- Section names listed individually
- Paper counts shown
- Word count displayed
- Citation count shown

### Visual Feedback
- Agent panel shows active agent (blue glow)
- Completed agents show green checkmark
- Logs have colored left borders
- Hover over logs for subtle highlight

## 🧪 Test the System

### Quick Test (Terminal)
```bash
cd backend
python test_streaming_logs.py
```

Expected output: Colored terminal logs with timestamps showing full research flow.

### Browser Test
1. Open http://localhost:3000
2. Enter "Test Query"
3. Watch for:
   - ✅ Logs appear in real-time
   - ✅ Timestamps are correct
   - ✅ Colors are applied
   - ✅ Auto-scroll works
   - ✅ Agent status updates
   - ✅ Report appears at end

## 🐛 Troubleshooting

### No Logs Appearing
**Check**:
1. Backend running? (Should show on port 8000)
2. Browser console errors? (F12 to open)
3. SSE connection established? (Check Network tab)

**Fix**: Restart both servers (Ctrl+C, then start again)

### Logs Not Color-Coded
**Check**: Frontend loaded latest code?

**Fix**:
```bash
cd frontend
rm -rf .next
npm run dev
```

### Auto-Scroll Not Working
**Check**: Are you scrolled to the bottom?

**Fix**: Scroll to bottom of logs panel, then new logs will auto-scroll.

## 📱 Mobile Experience

Works great on mobile too!

- Agent panel stacks on top
- Logs panel below
- Touch-friendly scrolling
- Same color coding
- Responsive design

## 🎓 Tips

1. **Watch the timestamps** - See which agents take longest
2. **Read the section names** - Planner creates strategic research plan
3. **Check paper counts** - Paper Analyzer finds academic sources
4. **Note word count** - Writer generates comprehensive report
5. **Count citations** - Citation Agent adds proper references

## 🚦 Status Indicators

### In Progress
- Agent panel: Blue background, spinning icon
- Log entry: Blue text with emoji

### Completed
- Agent panel: Green background, checkmark icon
- Log entry: Green text with ✅

### Error
- Log entry: Red text with ❌
- Research stops, error shown

## 🎬 Example Session

**Query**: "Deep Learning"

**What Happens**:
1. **[0s]** You click send
2. **[1s]** 🧠 Planner creates 6 sections
3. **[6s]** 🔍 Researcher searches web (5 results × 6 sections)
4. **[20s]** 📖 Paper Analyzer finds 30 academic papers
5. **[25s]** ✨ Insight Extractor pulls key insights
6. **[27s]** 🔧 Source Ranker evaluates quality
7. **[30s]** 🛡️ Critic validates findings
8. **[32s]** ✍️ Writer generates ~500 word report
9. **[35s]** 💬 Citation Agent adds 18 citations
10. **[35s]** 🎉 Report displayed with references!

**Total**: ~35 seconds from query to complete report

## ✨ Enjoy!

You now have a premium AI research assistant with:
- ✅ Real-time progress visibility
- ✅ Precise performance tracking
- ✅ Beautiful, animated UI
- ✅ Professional citations
- ✅ Multi-source research

Start researching! 🚀

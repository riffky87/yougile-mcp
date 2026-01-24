# Fix: Boolean Validation Error in MCP Tools

## Problem

When calling Yougile MCP tools like `yougile_list_boards` or `yougile_list_projects`, the error occurred:
```
deleted Input should be a valid boolean
```

## Root Cause

The Pydantic models used for MCP tool return types had non-optional boolean fields with default values:

```python
class YouGileBaseModel(BaseModel):
    id: str
    timestamp: Optional[datetime] = None
    deleted: bool = Field(False, ...)  # ❌ Not optional
```

When the YouGile API returns data without a `deleted` field (which is common), Pydantic validation fails because:
1. The field is marked as required (not `Optional`)
2. The MCP framework validates the return type
3. Missing fields cause validation errors

## Solution

Changed all boolean fields with defaults to be `Optional[bool]`:

```python
class YouGileBaseModel(BaseModel):
    id: str
    timestamp: Optional[datetime] = None
    deleted: Optional[bool] = Field(False, ...)  # ✅ Optional
```

## Files Changed

**`src/core/models.py`:**
- `YouGileBaseModel.deleted`: `bool` → `Optional[bool]`
- `TaskDeadline.with_time`: `bool` → `Optional[bool]`
- `TaskDeadline.deleted`: `bool` → `Optional[bool]`
- `TaskTimeTracking.deleted`: `bool` → `Optional[bool]`
- `TaskStopwatch.running`: `bool` → `Optional[bool]`
- `TaskStopwatch.deleted`: `bool` → `Optional[bool]`
- `TaskChecklist.is_completed`: `bool` → `Optional[bool]`

## Why This Works

1. **API Flexibility**: YouGile API may or may not include these fields in responses
2. **Default Values**: The `Field(False, ...)` still provides a default when the field is missing
3. **Type Safety**: `Optional[bool]` allows `None`, `True`, or `False`
4. **MCP Validation**: The MCP framework can now validate responses even when fields are missing

## Testing

After this fix, these tools should work:
- `yougile_list_boards`
- `yougile_list_projects`
- `yougile_list_tasks`
- `yougile_get_task`
- All other tools that return models with boolean fields

## Deployment

1. Commit and push changes to yougile-mcp repo
2. Rebuild Docker image with cache busting:
   ```bash
   docker build --build-arg YOUGILE_CACHE_BUST=$(date +%s) -f build/agent.dockerfile -t kingmaker-code-agent:latest .
   ```
3. Test with: "What yougile boards are there?"

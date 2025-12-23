# VLA Data Model and Flow Architecture

## Core Entities

### Voice Command
- **Fields**:
  - `id`: Unique identifier for the command
  - `audio_data`: Raw audio input (base64 encoded)
  - `transcript`: Text transcription from Whisper
  - `timestamp`: When the command was received
  - `confidence`: Confidence score from speech recognition
  - `intent`: Extracted intent from LLM processing
  - `entities`: Identified entities (objects, locations, actions)

### Intent
- **Fields**:
  - `type`: Command type (navigation, manipulation, query, etc.)
  - `action_sequence`: Planned sequence of ROS 2 actions
  - `parameters`: Action parameters (coordinates, object names, etc.)
  - `context`: Environmental context needed for execution
  - `validation_status`: Whether the intent can be executed safely

### ROS 2 Action Plan
- **Fields**:
  - `id`: Unique plan identifier
  - `actions`: Array of ROS 2 action definitions
  - `dependencies`: Action execution dependencies
  - `timeout`: Maximum time for plan execution
  - `recovery_steps`: Actions to take if primary action fails
  - `validation_rules`: Safety and feasibility checks

### Perception Data
- **Fields**:
  - `timestamp`: When data was captured
  - `image_data`: Camera image data
  - `depth_data`: Depth sensor readings
  - `point_cloud`: 3D point cloud data
  - `detected_objects`: Array of recognized objects with poses
  - `spatial_relationships`: Object-to-object and object-to-robot relationships

### Action Execution Result
- **Fields**:
  - `action_id`: Identifier of the executed action
  - `status`: Success, failure, or partial completion
  - `execution_time`: Time taken to complete the action
  - `feedback`: ROS 2 action feedback message
  - `error_code`: Error code if action failed
  - `recovery_needed`: Whether recovery action is required

## Data Flow Architecture

### Language Signal Flow

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Voice Input   │───▶│  Whisper Speech  │───▶│ Intent Extractor│
│   (Audio)       │    │ Recognition      │    │ (LLM Processing)│
│   - audio_data  │    │   - transcript   │    │   - intent      │
│   - timestamp   │    │   - confidence   │    │   - entities    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                              │
                                                              ▼
                                               ┌─────────────────┐
                                               │ Task Decomposer │
                                               │ (LLM Planning)  │
                                               │ - action_seq    │
                                               │ - parameters    │
                                               │ - context       │
                                               └─────────────────┘
                                                              │
                                                              ▼
                                               ┌─────────────────┐
                                               │ Action Validator│
                                               │ - safety check  │
                                               │ - feasibility   │
                                               │ - constraints   │
                                               └─────────────────┘
                                                              │
                                                              ▼
                                               ┌─────────────────┐
                                               │ ROS 2 Execution │
                                               │ - action plan   │
                                               │ - feedback loop │
                                               └─────────────────┘
```

### Vision Signal Flow

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Camera/Sensor  │───▶│  Perception      │───▶│ Object Detection│
│  - image_data   │    │  Processing      │    │  - objects      │
│  - depth_data   │    │   - filtering    │    │  - poses        │
│  - point_cloud  │    │   - segmentation │    │  - confidence   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                              │
                                                              ▼
                                      ┌─────────────────────────────────┐
                                      │ Spatial Relationship Analysis   │
                                      │ - object-to-object relations    │
                                      │ - object-to-robot relations     │
                                      │ - scene context                 │
                                      └─────────────────────────────────┘
                                                              │
                                                              ▼
                                      ┌─────────────────────────────────┐
                                      │ Vision-Language Fusion Layer    │
                                      │ - combine vision with language  │
                                      │ - contextual understanding      │
                                      │ - action context provision      │
                                      └─────────────────────────────────┘
```

### Robot Action Flow

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Action Plan    │───▶│  Action Validator│───▶│ Execution Queue │
│  - sequence     │    │  - safety check  │    │  - scheduling   │
│  - parameters   │    │  - feasibility   │    │  - coordination │
│  - constraints  │    │  - dependencies  │    │  - monitoring   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                              │
                                                              ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Simulation     │◀───│  ROS 2 Actions   │◀───│  Action Mapper  │
│  - state update │    │  - execution     │    │  - ROS mapping  │
│  - feedback     │    │  - monitoring    │    │  - parameter    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                              │
                                                              ▼
                                               ┌─────────────────┐
                                               │ Result Handler  │
                                               │ - status update │
                                               │ - error handling│
                                               │ - recovery plan │
                                               └─────────────────┘
```

## State Transitions

### Voice Command State Machine
```
RECEIVED → TRANSCRIBING → [TRANSCRIBED | TRANSCRIPTION_FAILED]
           ↓
    INTENT_PROCESSING → [INTENT_EXTRACTED | INTENT_FAILED]
           ↓
    TASK_DECOMPOSING → [TASK_DECOMPOSED | DECOMPOSITION_FAILED]
           ↓
    VALIDATING → [VALID | INVALID] → [EXECUTING | REJECTED]
```

### Action Plan State Machine
```
CREATED → VALIDATING → [VALID | INVALID]
           ↓
    SCHEDULING → SCHEDULED → EXECUTING → [COMPLETED | FAILED]
                                    ↓
                            [RECOVERING | NEEDS_REPLANNING]
```

## Validation Rules

### Input Validation
- Voice commands must have confidence score > 0.7
- Language commands must contain actionable verbs
- Vision data must be current (less than 1 second old)
- Action parameters must be within robot's physical limits

### Safety Constraints
- No actions that would cause robot to collide with obstacles
- Joint limits must not be exceeded
- Actions must be physically possible given current robot state
- Emergency stop capability must be available during execution

### Execution Constraints
- Action sequences must be executable within timeout limits
- Dependencies between actions must be satisfied
- Robot state must be valid for each action
- Recovery actions must be available for all risky operations

## Error Handling Strategies

### Speech Recognition Errors
- Low confidence transcription → Request repetition
- Unintelligible audio → Return error with suggestions
- API failures → Fallback to text input

### Intent Extraction Errors
- Ambiguous commands → Request clarification
- Unknown commands → Suggest valid alternatives
- LLM processing failures → Return to previous state

### Action Execution Errors
- Invalid action parameters → Return to planning phase
- Execution failures → Attempt recovery actions
- Safety constraint violations → Emergency stop

### Vision Processing Errors
- Object detection failures → Use alternative perception methods
- Outdated vision data → Request new data capture
- Spatial reasoning errors → Fall back to simple navigation
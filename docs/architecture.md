# Architecture Documentation

This document describes the architecture of the current project implementation in `main_dict.py`.

## Scope and assumptions

- The runtime is a single-module Pygame application.
- The primary execution path is `run()` (invoked from `if __name__ == "__main__":`).
- Behavioral logic includes lifespan filtering, flee behavior, chase behavior, movement updates, and rendering.

## Module dependency graph

```mermaid
flowchart LR
    App["Python Runtime"] --> Entry["__main__ Guard"]
    Entry --> Mod["main_dict.py"]
    Mod --> Pygame["pygame"]
    Mod --> Random["random"]
```

## High-level runtime flow

```mermaid
flowchart TD
    Start["Start Program"] --> Init["run(): Initialize Pygame, Screen, Clock, Font"]
    Init --> Create["create_squares(SQUARE_COUNT)"]
    Create --> Loop{"Main Loop Running?"}

    Loop -->|"yes"| Events["handle_events()"]
    Events --> Alive["Filter Non-Expired Squares via is_expired()"]
    Alive --> Respawn["Respawn via create_square() until SQUARE_COUNT"]
    Respawn --> Behavior["Pairwise Behavior Check"]
    Behavior --> Branch{"size comparison + radius checks"}
    Branch -->|"small near big"| Flee["flee_away(small, big)"]
    Branch -->|"big near small and not fleeing"| Chase["chase_towards(big, small)"]
    Branch -->|"no condition met"| Skip["No velocity override"]

    Flee --> Update["update_square() for each square"]
    Chase --> Update
    Skip --> Update

    Update --> Draw["draw_square() for each square"]
    Draw --> Hud["Render FPS and Square Count"]
    Hud --> Present["display.flip() + clock.tick(FPS)"]
    Present --> Loop

    Loop -->|"no"| End["pygame.quit()"]
```

## Function-level call graph

```mermaid
flowchart TD
    Main["__main__"] --> Run["run()"]

    Run --> HandleEvents["handle_events()"]
    Run --> CreateSquares["create_squares(count)"]
    Run --> IsExpired["is_expired(square)"]
    Run --> CreateSquare["create_square()"]
    Run --> IsCloseEnough["is_close_enough(square1, square2, radius)"]
    Run --> FleeAway["flee_away(small_square, big_square)"]
    Run --> ChaseTowards["chase_towards(bigger_square, smaller_square)"]
    Run --> UpdateSquare["update_square(square)"]
    Run --> DrawSquare["draw_square(screen, square)"]

    CreateSquares --> CreateSquare
    CreateSquare --> RandomColor["random_color()"]
    FleeAway --> CalculateDistance["calculate_distance(pos1, pos2)"]
    ChaseTowards --> CalculateDistance
```

## Primary execution sequence (full frame path)

```mermaid
sequenceDiagram
    participant RT as "Python Runtime"
    participant APP as "run()"
    participant EVT as "handle_events()"
    participant LIFE as "is_expired()"
    participant AI as "is_close_enough() / flee_away() / chase_towards()"
    participant PHYS as "update_square()"
    participant REND as "draw_square() + HUD + display"

    RT->>APP: "Call run() from __main__"
    APP->>APP: "Initialize pygame/screen/clock/font"
    APP->>APP: "create_squares(SQUARE_COUNT)"

    loop "Each frame while running"
        APP->>EVT: "Poll events"
        EVT-->>APP: "running flag"

        APP->>LIFE: "Check each square lifespan"
        alt "square expired"
            LIFE-->>APP: "exclude square"
        else "square alive"
            LIFE-->>APP: "keep square"
        end

        APP->>APP: "Respawn new squares until count is stable"

        loop "For each (small, big) pair"
            APP->>AI: "size/radius checks"
            alt "small is close to bigger square"
                AI->>AI: "flee_away(): set small vx/vy"
            else "bigger is close to smaller square"
                AI->>AI: "chase_towards(): set big vx/vy"
            else "neither condition"
                AI-->>APP: "no override"
            end
        end

        APP->>PHYS: "update_square() for all squares"
        APP->>REND: "draw squares, draw FPS/count, flip, tick"
    end

    APP-->>RT: "Quit pygame and return"
```

## Data model snapshot

The application uses plain dictionaries for entities. A square contains:

- Position: `x`, `y`
- Velocity: `vx`, `vy`
- Visual state: `size`, `color`
- Lifecycle state: `created_at`, `lifespan`

This dictionary is read and mutated by multiple functions (`is_expired`, movement and behavior functions, and rendering).

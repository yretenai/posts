---
title: some notes about gaming on linux
short: this is mostly so i don't forget
date: 2024-06-22 4:36 AM
updated: 2024-06-22 9:51 AM
---

I recently migrated to using Linux full time.
You need to not look far to find an ocean of reasons why Windows has been a bit miserable.

This post mainly serves as a logbook for fixes and workarounds for making games (and some applications) work on Linux.

## EAC "Failed to Intialize Dependencies" error

This is likely due to a `SDL_VIDEODRIVER` and/or `SDL_VIDEO_DRIVER` environment variable being present.

Try using the following launch arguments:

`env --unset=SDL_VIDEODRIVER --unset=SDL_VIDEO_DRIVER %command%`

Alternatively, set the variable to an empty string in whatever launch manager you're using (Heroic, Lutris).

## Enabling DX12 Ray Tracing

If you have a ray tracing capable GPU (RTX 2000 or newer, RX 6800 or newer)
you might be able to tell Mesa and VKD3D that ray-tracing can be enabled by using the following launch arguments:

`env RADV_PERFTEST=rt VKD3D_CONFIG=dxr VKD3D_FEATURE_LEVEL=12_2 %command%`

If you have an older GPU you can try:

`env RADV_PERFTEST=emulate_rt VKD3D_CONFIG=dxr VKD3D_FEATURE_LEVEL=12_2 %command%`

This assumes you have a relatively recent VKD3D and Mesa installation,
and the game has to support ray tracing in any capacity (i.e. World of Warcraft, Ratchet and Clank: Rift Apart)

## Windows-only Third-Party Mod Tooling

You can add the mod tools as a non-steam game, given it has a GUI.

When you do, force it to use **the same compatability tools as the game** and set the launch arguments to:

`env STEAM_COMPAT_DATA_PATH="~/.steam/root/steamapps/compatdata/489830" %command%`

You may need to install more dependencies like .NET 4.8/6.0, etc via protontricks, select the game *not* the non-steam app when installing.

Change `~/.steam/root/steamapps` to the SteamLibrary steamapps folder if installed in a steam library folder.

Change 489830 to match the steam id of the mod tool the game is for, 489830 is Skyrim SE/AE.
It is the number after `/app/` in the Steam store link, alternatively look it up on SteamDB.

## Game-Specific Fixes

### Dauntless

If you randomly crash, it might be because of stack smashing due to a race condition.

I have managed to reduce the frequency of crashes by limiting how many resources the game can use.

`env DXVK_CONFIG="dxvk.numCompilerThreads=1" WINE_CPU_TOPOLOGY="4:0,2,4,6" %command%`

If there is too much lag, you might want to redefine the CPU topology, i.e. `WINE_CPU_TOPOLOGY="8:0,1,2,3,4,5,6,7"`

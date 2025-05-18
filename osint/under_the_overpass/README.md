# Under the Overpass
Description:
```markdown
We have reports that an international spy, traveling under the name Cameron Joseph Snider, may be attempting to sell government secrets to a foreign government. His passport recently got pinged attempting to enter Germany, and we believe he is currently in Berlin attempting to meet his contacts at a foreign embassy. We need you to find out what country's embassy he is visiting, as well as how many security cameras are within 100 meters of this embassy.

His last emails mention having a bad toothache, and needing to schedule a visit with the dentist's office next door to the embassy he is at. He is also staying at a hotel that is on the other side of the embassy.

To help you find him in time, we are giving you special access to a secret government program. Good luck.

https://overpass-turbo.eu/

Flag format: `byuctf{Country_Name:Number of Cameras}`

Example: `byuctf{France:59}`
```

**Author**: `The Camel`

## Writeup
1. First, we need to craft an Overpass Turbo query to find all diplomatic offices in Berlin:
    ```json
    [out:json][timeout:25];
    {{geocodeArea:Berlin}}->.searchArea; (
    nwr["amenity"="embassy"](area.searchArea);
    nwr["office"="diplomatic"](area.searchArea); ); out
    center;
    ```
2. Looking for an embassy next to a dentist office gives us the embassy for El Salvador.
3. Finally, creating a query to give us every security camera within 100 meters of this embassy returns 10 cameras:
    ```json
    [out:json][timeout:25];
    // Search for surveillance devices within 100m of
    given coords
    (
    nwr(around:100, 52.5287089,
    13.3800402)["man_made"="surveillance"];
    nwr(around:100, 52.5287089,
    13.3800402)["surveillance"];
    );
    out body;
    ```

**Flag** - `byuctf{El_Salvador:10}`
# SOP 03 Output: Asset Generation for "First Spark"

## Part 1: The Manifest

### Cast (Character Variants with Specific Poses):
1. **Juvenile Pikachu (Walking Forward)** - Small frame, cautious gait, ears twitching
2. **Juvenile Pikachu (Crouch Position)** - Low to ground, focused, preparing to strike
3. **Juvenile Pikachu (Capacitor Charging)** - Close-up face, cheeks glowing intensely
4. **Juvenile Pikachu (Standing Defeated)** - Ears drooping, exhausted posture
5. **Juvenile Pikachu (Face Close-Up Exhausted)** - Macro of face showing defeat
6. **Elder Pikachu (Perched Alert)** - On rock, watching, static fur moving
7. **Elder Pikachu (Mid-Leap)** - Descending in coordinated attack pattern
8. **Elder Pikachu (Defensive Stance)** - In circular formation, facing outward
9. **Elder Pikachu (Teaching Pose)** - Paw adjusting juvenile's stance
10. **Fearow (Shadow Silhouette)** - Backlit dark shape with talons visible
11. **Fearow (Gliding Past)** - Mid-flight, wings extended, hunting focus
12. **Fearow (Braking)** - Wings pulled back sharply, retreating

### Props (Macro Subjects):
1. **Bark Beetles (Living Swarm)** - Crawling on rotting wood, iridescent carapaces
2. **Decaying Log (Pre-Explosion)** - Moss-covered, fungal growth, beetles visible
3. **Charred Beetle Corpses** - Scattered, blackened remains

### Sets (Location States):
1. **Pristine Misty Forest (Dawn)** - Undisturbed, thick fog, water droplets on ferns
2. **Forest Floor (Beetle Log Area)** - Focus on decaying log in undergrowth
3. **Electrical Flash (Pure Energy)** - White-blue plasma blast moment
4. **Log Explosion (Debris Mid-Air)** - Splinters frozen in explosion sphere
5. **Smoking Crater (Post-Explosion)** - Charred ground, fires burning, steam rising
6. **Defensive Formation Ground** - Circular scorch pattern from electrical discharge
7. **Forest Edge (Colony Together)** - Moss rock, dawn breaking through canopy

---

## Part 2: Clip-to-Asset Mapping Table

| Clip # | Shot Type | Asset(s) Required |
| :--- | :--- | :--- |
| 01 | Wide | Pristine Misty Forest (Environment Plate) |
| 02 | Low Tracking | Juvenile Pikachu (Walking Forward) + Pristine Forest Plate |
| 03 | Medium | Elder Pikachu (Perched Alert) + Pristine Forest Plate |
| 04 | Macro | Bark Beetles (Living Swarm) + Decaying Log (Pre-Explosion) |
| 05 | Close-Up | Juvenile Pikachu (Crouch Position) + Forest Floor Plate |
| 06 | Close-Up | Juvenile Pikachu (Capacitor Charging - Face) |
| 07 | Action | Electrical Flash (Pure Energy) - standalone VFX element |
| 08 | Wide | Log Explosion (Debris Mid-Air) - standalone action plate |
| 09 | Medium | Smoking Crater (Post-Explosion) + Juvenile Pikachu (Standing Defeated) |
| 10 | Close-Up | Juvenile Pikachu (Face Close-Up Exhausted) |
| 11 | POV Up | Fearow (Shadow Silhouette) - backlit element |
| 12 | Tracking | Fearow (Gliding Past) + Smoking Crater Background |
| 13 | Wide | Elder Pikachu (Mid-Leap) x3 + Smoking Crater Background |
| 14 | Overhead | Elder Pikachu (Defensive Stance) x4 + Juvenile (center) + Defensive Formation Ground |
| 15 | Medium Circle | Elder Pikachu (Defensive Stance) x4 + Electrical dome VFX |
| 16 | Close-Up | Fearow (Braking) + Electrical field distortion |
| 17 | Macro | Elder Pikachu (Teaching Pose) + Juvenile + Beetles + Forest Floor |
| 18 | Wide | Elder Pikachu (Perched Alert) x4 + Juvenile + Forest Edge Plate |

**Total Unique Assets:** 12 characters/creatures + 3 props + 7 environments = **22 total assets**

---

## Part 3: The Global Atmosphere Block

```
Early morning dawn light in temperate mixed forest, 15 minutes post-rainfall. Thick volumetric fog rolling at ground level through moss-covered deciduous trees, humidity 90%, every surface glistening with water droplets catching first golden sunlight. Diffused sunrise light filtering through dense canopy creating god rays and soft shadows with blue-green ambient fill light. Post-storm atmosphere with ozone residue creating faint metallic shimmer in mist. Shot on 35mm anamorphic lens with shallow depth of field, cinematic bokeh, atmospheric perspective showing layered depth. Color temperature cool blue-green (5000K) in shadows warming to golden highlights (6500K) where sunlight penetrates. Mist has weight and slow movement.
```

---

## Part 4: Master Prompts (Nano Bananao - Code Blocks)

### Characters

#### 1. Juvenile Pikachu (Walking Forward)

```
A hyper-realistic juvenile Pikachu in walking stance moving forward cautiously. Body structure of young American pika with compact muscular haunches, small frame showing inexperience. Walking pose with one front paw raised mid-step, weight balanced, tail held low horizontal for balance. Short coarse yellow fur with static-charged bristles naturally standing on end like wool carpet texture, rubberized black-tipped ears with matte neoprene-like texture, glossy bio-crystalline red cheek capacitor nodes smooth and faintly glowing amber, small calloused footpads. Eyes large and alert but nervous, ears twitching position. Wet ferns and undergrowth at ground level around feet. Early morning dawn light in temperate mixed forest, 15 minutes post-rainfall. Thick volumetric fog rolling at ground level through moss-covered deciduous trees, humidity 90%, every surface glistening with water droplets catching first golden sunlight. Diffused sunrise light filtering through dense canopy creating god rays and soft shadows with blue-green ambient fill light. Post-storm atmosphere with ozone residue creating faint metallic shimmer in mist. Shot on 35mm anamorphic lens with shallow depth of field, cinematic bokeh, atmospheric perspective showing layered depth. Color temperature cool blue-green (5000K) in shadows warming to golden highlights (6500K) where sunlight penetrates. Mist has weight and slow movement. Unreal Engine 5, 8k photorealistic texturing, National Geographic wildlife photography style, cinematic lighting, subsurface scattering on fur, depth of field --ar 16:9 --no anime, cartoon, illustration, drawing, cel-shaded, 3d model, render, low poly, text, watermark, Pokemon game style, motion blur
```
**Suggested filename:** `pikachu_juvenile_walking.png`

#### 2. Juvenile Pikachu (Crouch Position)

```
A hyper-realistic juvenile Pikachu in low crouch hunting position. Body structure of young American pika, small compact frame low to ground in stable crouched pose. Weight distributed evenly on all four paws, body tense and coiled, tail curved along ground. Eyes narrowed in concentration, ears forward and alert, face showing determination. Short coarse yellow fur with static-charged bristles texture like wool carpet, rubberized black-tipped ears with matte neoprene texture, glossy bio-crystalline red cheek capacitor nodes beginning to glow faint amber. Small calloused footpads gripping ground. Surrounded by wet undergrowth, backlit by dawn light filtering through mist. Early morning dawn light in temperate mixed forest, 15 minutes post-rainfall. Thick volumetric fog rolling at ground level through moss-covered deciduous trees, humidity 90%, every surface glistening with water droplets catching first golden sunlight. Diffused sunrise light filtering through dense canopy creating god rays and soft shadows with blue-green ambient fill light. Post-storm atmosphere with ozone residue creating faint metallic shimmer in mist. Shot on 35mm anamorphic lens with shallow depth of field, cinematic bokeh, atmospheric perspective showing layered depth. Color temperature cool blue-green (5000K) in shadows warming to golden highlights (6500K) where sunlight penetrates. Mist has weight and slow movement. Unreal Engine 5, 8k photorealistic texturing, National Geographic wildlife photography style, cinematic lighting, subsurface scattering on fur, depth of field --ar 16:9 --no anime, cartoon, illustration, drawing, cel-shaded, 3d model, render, low poly, text, watermark, Pokemon game style, motion blur
```
**Suggested filename:** `pikachu_juvenile_crouch.png`

#### 3. Juvenile Pikachu (Capacitor Charging - Face Close-Up)

```
Extreme close-up of juvenile Pikachu's face during electrical charge buildup. Face-forward view showing large dark eyes narrowed in concentration with determination, glossy bio-crystalline red cheek capacitor nodes glowing intensely transitioning from amber to bright yellow-white with visible internal energy, short coarse yellow fur beginning to stand on end from static electricity with individual bristles visible. Rubberized black-tipped ears partially in frame at top edges with matte neoprene texture. Fur texture like wool carpet with static charge causing micro-movements. Water droplets on fur starting to evaporate from heat buildup creating small wisps of steam. Ozone residue creating faint glow around face. Backlit by morning sun breaking through fog creating rim lighting on fur edges. Early morning dawn light in temperate mixed forest, 15 minutes post-rainfall. Thick volumetric fog in background slightly out of focus. Humidity 90% visible as moisture in air. Shot on 35mm anamorphic lens with extremely shallow depth of field, bokeh background. Color temperature cool blue-green ambient with warm golden rim light. Unreal Engine 5, 8k macro photography, National Geographic wildlife extreme close-up style, cinematic lighting, subsurface scattering showing skin translucency, depth of field --ar 16:9 --no anime, cartoon, illustration, drawing, cel-shaded, 3d model, render, low poly, text, watermark, Pokemon game style, motion blur
```
**Suggested filename:** `pikachu_juvenile_charging_face.png`

#### 4. Juvenile Pikachu (Standing Defeated)

```
A hyper-realistic juvenile Pikachu in defeated standing posture at edge of smoking crater. Small compact frame standing upright but slouched, shoulders slumped forward, weight shifted onto back legs showing exhaustion. Ears drooping downward, tail dragging on ground behind, head lowered staring at destruction. Short coarse yellow fur slightly matted and disheveled, rubberized black-tipped ears limp, glossy bio-crystalline red cheek capacitor nodes dim and barely glowing showing depleted energy reserves. Small calloused footpads on scorched ground. Body language communicating complete defeat and exhaustion without being overly dramatic. Charred debris and smoke wisps around feet, small fires burning in background on wood fragments. Early morning light now fully illuminating scene, mist mixing with smoke. Humid post-storm atmosphere. Shot on 35mm anamorphic lens with shallow depth of field, smoking crater background slightly out of focus. Color temperature neutral with orange fire glow accents. Unreal Engine 5, 8k photorealistic texturing, National Geographic wildlife photography style, cinematic lighting, subsurface scattering on fur, depth of field --ar 16:9 --no anime, cartoon, illustration, drawing, cel-shaded, 3d model, render, low poly, text, watermark, Pokemon game style, motion blur
```
**Suggested filename:** `pikachu_juvenile_defeated.png`

#### 5. Juvenile Pikachu (Face Close-Up Exhausted)

```
Extreme close-up of juvenile Pikachu's exhausted face. Large dark eyes with defeated expression, pupils dilated, staring downward at destruction. Ears visibly drooping to sides of head, tips curving downward. Glossy bio-crystalline red cheek capacitor nodes dimmed to barely visible amber glow showing complete energy depletion. Short coarse yellow fur slightly matted, individual bristles no longer standing from static. Rubberized black-tipped ears limp with matte neoprene texture. Breathing visible through slight chest movement, small wisps of smoke crossing frame in front of face. Ozone residue smell implied by faint metallic shimmer. Morning light fully illuminating features, no more backlight. Face showing physical and emotional exhaustion through body language alone. Early morning temperate forest light, smoke and steam in air creating atmospheric haze. Shot on 35mm anamorphic lens with extremely shallow depth of field, bokeh background of smoking destruction. Color temperature neutral warm. Unreal Engine 5, 8k macro photography, National Geographic wildlife extreme close-up style, cinematic lighting, subsurface scattering, depth of field --ar 16:9 --no anime, cartoon, illustration, drawing, cel-shaded, 3d model, render, low poly, text, watermark, Pokemon game style, motion blur
```
**Suggested filename:** `pikachu_juvenile_exhausted_face.png`

#### 6. Elder Pikachu (Perched Alert)

```
A hyper-realistic elder Pikachu in alert perched stance on moss-covered rock formation. Larger heavier build than juvenile showing mature American pika structure with pronounced muscular haunches. Perched position with weight balanced on rock, body upright and commanding, tail thick and held confidently. Eyes sharp and focused watching downward intently, ears forward in alert position. Coarse yellow fur with static-charged bristles texture rougher and more weathered showing years, subtle scars visible beneath fur on shoulders from past battles. Rubberized black-tipped ears showing small chips and wear at edges, glossy bio-crystalline red cheek capacitor nodes glowing brighter indicating greater charge capacity. Heavily calloused scorched footpads from years of electrical grounding. Battle-experienced features without being grotesque, commanding presence. Moss-covered rock with lichen visible beneath paws. Partially obscured by morning mist at lower elevations. Early morning dawn light in temperate mixed forest, 15 minutes post-rainfall. Thick volumetric fog at ground level, humidity 90%, surfaces glistening. Diffused sunrise light creating god rays, soft shadows with blue-green ambient fill. Post-storm atmosphere with ozone residue in mist. Shot on 35mm anamorphic lens with shallow depth of field, cinematic bokeh. Color temperature cool blue-green warming to golden highlights. Unreal Engine 5, 8k photorealistic texturing, National Geographic wildlife photography style, cinematic lighting, subsurface scattering on fur, depth of field --ar 16:9 --no anime, cartoon, illustration, drawing, cel-shaded, 3d model, render, low poly, text, watermark, Pokemon game style, motion blur
```
**Suggested filename:** `pikachu_elder_perched.png`

#### 7. Elder Pikachu (Mid-Leap Descending)

```
A hyper-realistic elder Pikachu frozen mid-leap descending from elevated position. Larger build showing mature American pika structure in dynamic airborne pose, body angled 45 degrees downward toward camera. All four legs extended in coordinated leap pattern, tail streaming behind for balance. Eyes focused downward with intensity, ears pinned back from air resistance, mouth slightly open showing determination. Coarse yellow fur bristling and standing on end from static electricity, individual fur strands visible in motion. Rubberized black-tipped ears with worn edges, glossy bio-crystalline red cheek capacitor nodes glowing bright yellow-white showing active charge. Heavily calloused footpads visible on extended paws. Electricity already arcing between fur strands creating small blue-white plasma threads. Veteran warrior in action showing precision and speed. Mist parting around body from movement, debris from destroyed log still settling in background slightly out of focus. Early morning light, post-explosion atmosphere with smoke mixing with fog. Shot on 35mm anamorphic lens capturing moment of decisive action, shallow depth of field. Color temperature neutral with electrical blue-white accents. Unreal Engine 5, 8k photorealistic texturing, National Geographic wildlife action photography style, cinematic lighting, subsurface scattering on fur, depth of field --ar 16:9 --no anime, cartoon, illustration, drawing, cel-shaded, 3d model, render, low poly, text, watermark, Pokemon game style, motion blur
```
**Suggested filename:** `pikachu_elder_leap.png`

#### 8. Elder Pikachu (Defensive Stance)

```
A hyper-realistic elder Pikachu in defensive formation stance on scorched ground. Larger mature build in stable standing position facing outward from center, body low and coiled ready to defend. Weight evenly distributed, tail pointed inward toward formation center behind it. Ears forward in alert position, eyes focused outward scanning for threats, back arched slightly creating defensive profile. Coarse yellow fur bristling and standing completely vertical from electrical charge creating spiky silhouette. Rubberized black-tipped ears with battle wear, glossy bio-crystalline red cheek capacitor nodes pulsing bright yellow-white in rhythm with other colony members. Heavily calloused footpads gripping scorched earth. Electricity arcing from fur creating blue-white plasma glow around body. Synchronized posture showing rehearsed military precision. Standing on circular scorch pattern ground showing previous electrical discharge marks. Ozone thick in air creating visible ionization distortion. Mist beginning to ionize around electrical field. Early morning light, post-explosion clearing atmosphere. Shot on 35mm anamorphic lens from ground level, shallow depth of field. Color temperature neutral with blue-white electrical glow. Unreal Engine 5, 8k photorealistic texturing, National Geographic wildlife photography style, cinematic lighting, subsurface scattering on fur, depth of field --ar 16:9 --no anime, cartoon, illustration, drawing, cel-shaded, 3d model, render, low poly, text, watermark, Pokemon game style, motion blur
```
**Suggested filename:** `pikachu_elder_defensive.png`

#### 9. Elder Pikachu (Teaching Pose)

```
A hyper-realistic elder Pikachu in gentle teaching stance with paw extended. Larger mature build in calm patient posture, standing close to juvenile, body relaxed but attentive. One front paw raised and extended forward making gentle contact with juvenile's ear to adjust position, demonstrating proper hunting stance. Eyes soft and focused on teaching, ears in neutral forward position, face showing patience and mentorship. Coarse yellow fur settled naturally not bristling, static charge minimal. Rubberized black-tipped ears with battle wear showing experience, glossy bio-crystalline red cheek capacitor nodes glowing soft amber at rest. Heavily calloused footpads on forest floor. Subtle scars visible showing years of experience without being grotesque. Mentorship moment captured in body language - gentle correction, patient demonstration. Softer lighting as mist clears, new decaying log with fresh bark beetles visible slightly out of focus in background. Early morning light warmer as sunrise progresses. Humid forest atmosphere returning to normal after conflict. Shot on 35mm anamorphic lens with shallow depth of field, soft focus on background beetles. Color temperature warming to full sunrise golden hour. Unreal Engine 5, 8k photorealistic texturing, National Geographic wildlife photography style, cinematic lighting, subsurface scattering on fur, depth of field --ar 16:9 --no anime, cartoon, illustration, drawing, cel-shaded, 3d model, render, low poly, text, watermark, Pokemon game style, motion blur
```
**Suggested filename:** `pikachu_elder_teaching.png`

### Fearow Assets

#### 10. Fearow (Shadow Silhouette)

```
A hyper-realistic Fearow shown as dark silhouette backlit against bright morning sky. Skeletal structure of red-tailed hawk, 4-foot wingspan fully extended in descending glide position. Body shown as black shape against light with only key features visible: sharp hooked beak profile, extended talons spread wide showing individual claws, primary and secondary flight feathers creating distinct wing outline. Massive size emphasized by wingspan. Descending rapidly through thick volumetric mist layers, fog swirling in its wake from air displacement. Backlit by strong morning sun behind clouds creating dramatic rim lighting on wing edges and feather tips. Predator appearing as threatening dark shape from prey's ground-level POV. Talons clearly visible in silhouette reaching downward. Mist creating atmospheric layers showing depth of descent. Early morning light strong behind subject creating high contrast. Shot from ground level looking up, 35mm anamorphic lens capturing scale and threat. Color temperature cool blue mist with bright warm backlight. Unreal Engine 5, 8k photorealistic bird anatomy, National Geographic predator photography style, cinematic lighting, atmospheric depth, depth of field --ar 16:9 --no anime, cartoon, illustration, drawing, cel-shaded, 3d model, render, low poly, text, watermark, Pokemon game style, motion blur
```
**Suggested filename:** `fearow_shadow.png`

#### 11. Fearow (Gliding Past Camera)

```
A hyper-realistic Fearow in mid-glide flight past camera. Skeletal structure of red-tailed hawk, 4-foot wingspan fully extended in stable glide position. Sleek brown-red raptor plumage showing individual feather detail with barbs and rachis visible, cream-colored chest feathers, darker brown wing tips and tail feathers. Cruel hooked beak like eagle with sharp cutting edge, bright predatory yellow eyes with nictitating membrane partially visible, razor-sharp talons extended forward showing individual scales on feet. Body angled slightly downward in hunting dive, wings creating airflow visible through feather movement. Eyes locked downward on prey with intense predatory focus, no hesitation in expression. Individual primary and secondary flight feathers visible with slight gaps between showing wing anatomy. Feathers shifting subtly in wind resistance. Mist trailing behind from air displacement, smoke from crater visible in background out of focus. Early morning light fully illuminating plumage, showing texture and natural coloration. Apex aerial predator at hunting peak. Shot tracking alongside, 35mm anamorphic lens capturing motion and detail, shallow depth of field with smoking crater background. Color temperature neutral morning light with orange fire glow from background. Unreal Engine 5, 8k photorealistic bird anatomy, National Geographic predator photography style, cinematic lighting, subsurface scattering on feathers, depth of field --ar 16:9 --no anime, cartoon, illustration, drawing, cel-shaded, 3d model, render, low poly, text, watermark, Pokemon game style, motion blur
```
**Suggested filename:** `fearow_gliding.png`

#### 12. Fearow (Braking - Retreating)

```
A hyper-realistic Fearow pulling up sharply from dive in braking position. Skeletal structure of red-tailed hawk, 4-foot wingspan pulled back and cupped forward creating air resistance. Sleek brown-red raptor plumage with individual feathers ruffled and disturbed from sudden braking motion. Cruel hooked beak, bright yellow eyes widened in recognition of threat showing calculation and retreat decision. Talons retracting upward toward body, individual toe scales visible. Wings in full brake configuration with primary feathers splayed creating maximum drag, secondary feathers curved. Body posture shifted from dive to climb, head pulled back. Feathers visibly ruffled from proximity to electrical field, small static discharge arcs reaching toward it from below but not making contact. Expression showing predator intelligence - recognition that prey is now too dangerous. Individual feather details showing natural wear and flight stress. Mist ionized and distorted around electrical field below creating visible atmospheric distortion. Early morning light, electrical blue-white glow from below creating under-lighting on chest feathers. Shot at eye level with Fearow, 35mm anamorphic lens, shallow depth of field with electrical dome background slightly out of focus. Color temperature neutral with blue-white electrical accent lighting. Unreal Engine 5, 8k photorealistic bird anatomy, National Geographic predator photography style, cinematic lighting, subsurface scattering on feathers, depth of field --ar 16:9 --no anime, cartoon, illustration, drawing, cel-shaded, 3d model, render, low poly, text, watermark, Pokemon game style, motion blur
```
**Suggested filename:** `fearow_braking.png`

### Props

#### 13. Bark Beetles (Living Swarm)

```
Extreme macro close-up of bark beetle swarm actively crawling on heavily rotting wood surface. Multiple beetles visible in sharp focus showing anatomical detail: iridescent carapaces with metallic green-brown coloration reflecting light, individual segmented exoskeleton plates with natural chitinous shine, antennae actively twitching and sensing environment, compound eyes visible as tiny dark domes, six jointed legs with microscopic tarsal claws gripping wood texture. Beetles in constant subtle motion - legs moving, antennae probing, bodies crawling over each other. Wood surface showing advanced decomposition with exposed grain pattern, white and orange mycelium fungal growth in patches, deep cracks and fissures. Moisture beads visible on both beetles and bark creating wet sheen. Individual beetle ranging 3-5mm in size, multiple specimens creating swarm effect. Wood texture showing years of rot - dark brown to gray coloration, soft decomposed areas. Early morning dawn light in temperate mixed forest creating rim lighting on beetle carapaces. Humidity 90% visible as moisture. Shot with macro lens creating extremely shallow depth of field, only 2-3 beetles in perfect focus with others gradually softening. Color temperature cool with warm highlights on iridescent shells. Unreal Engine 5, 8k macro photography, National Geographic insect photography style, cinematic lighting, depth of field --ar 16:9 --no anime, cartoon, illustration, drawing, stylized, text, watermark, motion blur
```
**Suggested filename:** `prop_beetles_living.png`

#### 14. Decaying Log (Pre-Explosion)

```
Detailed shot of large decaying log lying on forest floor, approximately 3 feet diameter. Ancient wood heavily weathered showing deep vertical cracks and fissures throughout bark, thick vibrant green moss growth covering approximately 60% of visible surface with individual moss leaves visible, water droplets on moss catching morning light. Orange and white shelf fungi growing from sides in layered formations, visible wood rot with exposed grain showing dark brown to gray coloration with hollow sections. Bark beetles actively crawling on surface creating movement, small bore holes indicating insect activity with sawdust visible. Log surrounded by wet ferns with water droplets, fallen leaves creating natural forest floor texture, smaller twigs and debris. Wood texture showing years of slow decomposition, patches of white lichen growth. Fungal fruiting bodies in various stages. Everything glistening from recent rainfall. Early morning dawn light in temperate mixed forest, 15 minutes post-rainfall. Thick volumetric fog at ground level, humidity 90%, diffused golden sunlight filtering through canopy creating soft directional light on log surface. Post-storm atmosphere. Shot on 35mm anamorphic lens with moderate depth of field keeping entire log in focus, forest background softly out of focus. NO CHARACTERS visible. Color temperature cool blue-green in shadows with warm golden highlights where sun touches moss. Unreal Engine 5, 8k photogrammetry-quality wood and organic textures, National Geographic nature photography style, cinematic lighting, depth of field --ar 16:9 --no anime, cartoon, illustration, drawing, people, animals, Pokemon, characters, text, watermark, motion blur
```
**Suggested filename:** `prop_log_intact.png`

#### 15. Charred Beetle Corpses

```
Extreme macro close-up of incinerated bark beetle remains scattered on scorched wood surface. Multiple beetle corpses showing complete thermal destruction: blackened carapaces with charred matte finish instead of iridescent shine, exoskeleton segments cracked and broken from heat, legs curled inward in death pose, antennae burned away or fragmentary. Individual beetles approximately 3-5mm showing varying degrees of incineration - some completely carbonized, others with orange ember glow still fading in cracks. Scattered randomly across blackened wood showing blast pattern. Wood surface beneath showing lightning-strike crystallization patterns, deep char with orange glowing embers visible in deepest cracks. Ash particles settling on surface. Small wisps of smoke rising from hottest points. Surface still radiating heat visible through slight air distortion. Thermal destruction complete but recent - embers still active. Macro detail showing texture of carbonized organic material. Early morning light, post-explosion atmosphere with smoke and steam in air. Shot with macro lens creating shallow depth of field, 2-3 beetle corpses in sharp focus with others softening. Color temperature neutral with orange ember glow providing accent lighting. Unreal Engine 5, 8k macro photography, National Geographic disaster documentation style, cinematic lighting, depth of field --ar 16:9 --no anime, cartoon, illustration, drawing, stylized, people, animals, text, watermark, motion blur
```
**Suggested filename:** `prop_beetles_charred.png`

### Environment Plates (Clean - No Characters)

#### 16. Pristine Misty Forest (Dawn) - Environment Plate

```
Wide establishing shot of pristine undisturbed temperate mixed forest interior at dawn, completely empty of any creatures or characters. Ancient deciduous trees with thick trunks 2-3 feet diameter covered in vibrant green moss and gray-green lichen, rough bark texture showing deep vertical fissures and natural weathering. Dense undergrowth of wet ferns with individual fronds visible and water droplets on every leaf surface, fallen logs in various stages of decay showing moss coverage and fungal growth, decomposing leaf litter creating natural brown carpet on forest floor with small mushroom clusters growing from rotting wood. Exposed tree roots creating natural pathways and texture variation. Forest floor uneven with natural dips and rises. Everything glistening from recent heavy rainfall. Early morning dawn light in temperate mixed forest, 15 minutes post-rainfall. Thick volumetric fog rolling slowly at ground level between trees creating layered atmospheric depth, humidity 90% visible as heavy moisture in air. Diffused golden sunlight filtering through dense canopy in distinct god rays, soft shadows with cool blue-green ambient fill light from fog. Post-storm atmosphere with ozone residue creating faint metallic shimmer in mist. Mist has physical weight and slow deliberate movement. Shot on 35mm anamorphic lens with moderate depth of field, cinematic bokeh on distant trees, atmospheric perspective showing multiple layers of depth. Leading lines from fallen logs creating natural composition following rule of thirds. Completely devoid of any living creatures, Pokemon, or characters - pure environment. Color temperature cool blue-green (5000K) in shadows gradually warming to golden highlights (6500K) where sunlight penetrates fog. Unreal Engine 5, 8k environmental photography, National Geographic landscape photography style, volumetric fog rendering, cinematic lighting, depth of field --ar 16:9 --no anime, cartoon, illustration, drawing, people, animals, Pokemon, characters, creatures, text, watermark, motion blur
```
**Suggested filename:** `env_forest_pristine.png`

#### 17. Forest Floor (Beetle Log Area) - Environment Plate

```
Medium shot of forest floor focused on area around decaying log in thick undergrowth, completely empty of creatures. Ground-level perspective showing wet fern fronds in foreground with water droplets, moss-covered forest floor with decomposing leaf litter, small mushroom clusters, exposed roots creating natural texture. Decaying log visible as focal point with bark texture, moss growth, fungal brackets - approximately 3 feet diameter showing years of slow rot. Smaller branches and twigs scattered naturally. Ground showing natural unevenness with small dips where water collects. Everything saturated from recent rainfall creating high moisture content. Early morning dawn light filtering down through canopy creating dappled lighting pattern on forest floor. Thick volumetric fog at ground level creating atmospheric layering, humidity 90% visible as moisture in air. Soft directional light from one side creating gentle shadows, blue-green ambient fill from fog. Post-storm atmosphere with everything glistening. Shot on 35mm anamorphic lens with shallow depth of field, foreground ferns slightly soft, mid-ground log in sharp focus, background trees in soft bokeh. NO CHARACTERS, creatures, or Pokemon visible anywhere in frame - pure environmental background plate for compositing. Color temperature cool blue-green in shadows with warm golden highlights where sunlight reaches ground. Unreal Engine 5, 8k environmental photography, National Geographic nature photography style, volumetric fog, cinematic lighting, depth of field --ar 16:9 --no anime, cartoon, illustration, drawing, people, animals, Pokemon, characters, creatures, text, watermark, motion blur
```
**Suggested filename:** `env_forest_floor.png`

#### 18. Electrical Flash (Pure Energy) - VFX Element

```
Bright white-blue electrical plasma flash at peak intensity captured as single frozen moment. Pure energy discharge creating brilliant white core with blue-white corona expanding outward in sphere pattern. Plasma arc characteristics matching Tesla coil discharge - not cartoon lightning bolts. Electrical energy ionizing surrounding air creating visible distortion waves, mist being pushed outward by electromagnetic blast wave in expanding sphere. Ozone flash visible as white-blue luminescence. Energy discharge showing realistic physics - bright central point with gradually dimming corona, electrical tendrils branching outward following air ionization paths. No visible source creature - pure electrical phenomenon isolated. Surrounding mist catching light and showing blast wave displacement creating sphere of clear air at center with compressed fog wall at periphery. Heat distortion visible in air from energy release. Single moment of peak discharge frozen in time. Misty forest background barely visible through intense light, silhouettes of trees. Post-rainfall atmosphere creating high humidity for electrical conduction. Shot on 35mm anamorphic lens capturing wide view of energy sphere, exposure balanced to show both bright core and surrounding detail. White-blue core (10,000K color temperature) with yellow-orange corona edge (3000K) showing thermal spectrum. Unreal Engine 5, 8k VFX element, reference Tesla coil plasma discharge photography, cinematic lighting, volumetric light scattering --ar 16:9 --no anime, cartoon, illustration, drawing, stylized lightning, characters, text, watermark
```
**Suggested filename:** `env_electrical_flash.png`

#### 19. Log Explosion (Debris Mid-Air) - Action Plate

```
Wide shot of log explosion captured at peak moment with debris frozen mid-air in sphere blast pattern, no characters visible. Large decaying log exploding from center outward showing splinters and charred wood fragments scattered in perfect radial pattern flying outward in all directions. Individual wood pieces ranging from small splinters to large chunks silhouetted against bright white electrical flash at center. Bark beetles incinerated mid-air visible as small dark particles in blast sphere. Debris field approximately 10-foot diameter sphere. Wood fragments showing thermal damage - charred black surfaces with orange ember glow on edges, some pieces still on fire with small flames. Blast wave visible pushing mist outward creating compressed fog wall at periphery of explosion sphere. Central flash white-blue plasma creating bright backlight for debris. Heat distortion visible in air from energy and thermal release. Single frozen moment of peak explosion showing physics of radial force - every piece traveling outward from center point. Ground barely visible below showing forest floor. Atmospheric smoke and steam beginning to form. Post-rainfall forest background with mist being displaced by blast. Shot on 35mm anamorphic lens with high frame rate capture showing frozen action moment, moderate depth of field keeping debris field in focus. NO CHARACTERS or creatures visible - pure destruction event. Color temperature white-blue electrical core (10,000K) with orange fire glow on debris (3000K) against cool blue-green forest background (5000K). Unreal Engine 5, 8k action photography, reference controlled demolition footage, cinematic lighting, volumetric effects --ar 16:9 --no anime, cartoon, illustration, drawing, people, animals, Pokemon, characters, creatures, text, watermark
```
**Suggested filename:** `env_log_explosion.png`

#### 20. Smoking Crater (Post-Explosion) - Environment Plate

```
Medium shot of forest floor showing aftermath of electrical explosion with smoking crater and debris field, completely empty of creatures. Central crater approximately 2 feet deep and 12 feet diameter with loose scorched soil showing radial blast pattern from center outward. Ground surface charred black in immediate area with gradual transition to singed at periphery. Splintered charred wood fragments scattered throughout 10-foot radius - individual pieces showing black char with orange glowing embers visible in cracks and splits. Small active fires burning on larger wood pieces creating flickering orange light. White and gray smoke rising vertically from multiple points throughout debris field, steam mixing with smoke from moisture in hot debris. Ash particles floating and settling. Surrounding ferns and undergrowth singed and blackened at edges, leaves curled from heat. Pristine forest visible at frame edges showing stark contrast between destruction and nature. Ground still radiating heat visible through slight air distortion effect. Charred beetle corpses scattered on debris. Everything showing recent thermal event - embers still glowing, smoke still rising. Early morning light now fully illuminating scene without fog interference, smoke creating new atmospheric element. Post-explosion atmosphere mixing with forest humidity. Shot on 35mm anamorphic lens with moderate depth of field, crater center in sharp focus with background forest in soft bokeh. NO CHARACTERS, creatures, or Pokemon visible - pure environmental destruction plate for compositing. Color temperature neutral base (5500K) with orange fire/ember glow (3000K) and cool blue-green forest background (5000K). Unreal Engine 5, 8k environmental photography, National Geographic disaster documentation style, volumetric smoke rendering, cinematic lighting, depth of field --ar 16:9 --no anime, cartoon, illustration, drawing, people, animals, Pokemon, characters, creatures, text, watermark, motion blur
```
**Suggested filename:** `env_crater_smoking.png`

#### 21. Defensive Formation Ground - Environment Plate

```
Medium overhead shot of forest floor showing circular pattern of electrical discharge scarring on scorched ground, completely empty of creatures. Five distinct scorch marks arranged in perfect circle approximately 8 feet diameter, each mark showing deep black charring where Pikachu paws contacted ground. Tail-pointed-inward pattern visible with connecting burn marks between the five points showing electrical current flow paths. Ground between marks showing ionization effects - discolored soil with blue-gray tint, small electrical burn patterns creating fractal-like branching. Center of circle showing concentrated charring where juvenile stood. Soil surface fused and crystallized in hottest areas creating glass-like texture. Ozone-affected ground showing visible discoloration. Surrounding area with singed vegetation pushed outward from electromagnetic pulse - ferns blackened at tips, leaves scattered showing blast effect. Small wisps of smoke rising from hottest scorch points. Ground still showing residual heat glow in deepest char. Everything showing recent high-energy electrical discharge event. Forest floor texture transitioning from scorched center to normal at periphery. Ash and carbon residue visible. Early morning light, post-electrical event atmosphere with ionized air creating faint shimmer. Ozone concentration heavy creating metallic smell implied by visual distortion. Shot on 35mm anamorphic lens from overhead angle, moderate depth of field keeping entire circular pattern in focus, forest background in soft bokeh. NO CHARACTERS, creatures, or Pokemon visible - pure ground scarring environmental plate. Color temperature neutral (5500K) with faint blue-white residual electrical glow (8000K) in deepest scorch marks. Unreal Engine 5, 8k environmental photography, National Geographic natural phenomenon documentation style, cinematic lighting, depth of field --ar 16:9 --no anime, cartoon, illustration, drawing, people, animals, Pokemon, characters, creatures, text, watermark, motion blur
```
**Suggested filename:** `env_formation_ground.png`

#### 22. Forest Edge (Colony Together) - Environment Plate

```
Wide shot of forest edge at moss-covered rock formation with clearing visible beyond, completely empty of creatures. Large ancient moss rock formation approximately 4-5 feet tall serving as natural elevated platform, covered in thick vibrant green moss with lichen patches showing years of growth. Rock surface showing natural weathering, cracks, and texture variations. Forest edge transitioning from dense interior to more open area - forest canopy thinning allowing more direct sunlight penetration. Dawn light breaking through canopy in strong golden shafts creating dramatic god rays, mist dissipating as sun intensity increases. Background showing partial forest clearing with more open sky visible. Trees framing shot on sides creating natural vignette. Forest floor showing mixture of moss, ferns, exposed roots around rock base. Everything still glistening from morning dew but drying as sunlight strengthens. Morning atmosphere transitioning from cool blue pre-dawn to warm golden hour. Volumetric fog mostly cleared at this later morning hour, only thin wisps remaining at ground level. Rock formation provides natural elevated viewpoint over forest. Pristine peaceful environment showing morning awakening. Shot on 35mm anamorphic lens with moderate depth of field, rock formation in sharp focus, forest background with cinematic bokeh showing depth. NO CHARACTERS, creatures, or Pokemon visible anywhere - pure environmental background plate for compositing final colony scene. Color temperature warming significantly to full sunrise golden hour (6500K-7000K), cool blue shadows (5000K) still present but diminishing. Sky visible through canopy showing blue with warm sunrise tones. Unreal Engine 5, 8k environmental photography, National Geographic landscape photography style, volumetric lighting with god rays, cinematic lighting, depth of field --ar 16:9 --no anime, cartoon, illustration, drawing, people, animals, Pokemon, characters, creatures, text, watermark, motion blur
```
**Suggested filename:** `env_forest_edge.png`

---

## Production File Naming and Asset Organization

**Character Assets (12 files):**
1. `pikachu_juvenile_walking.png`
2. `pikachu_juvenile_crouch.png`
3. `pikachu_juvenile_charging_face.png`
4. `pikachu_juvenile_defeated.png`
5. `pikachu_juvenile_exhausted_face.png`
6. `pikachu_elder_perched.png`
7. `pikachu_elder_leap.png`
8. `pikachu_elder_defensive.png`
9. `pikachu_elder_teaching.png`
10. `fearow_shadow.png`
11. `fearow_gliding.png`
12. `fearow_braking.png`

**Prop Assets (3 files):**
13. `prop_beetles_living.png`
14. `prop_log_intact.png`
15. `prop_beetles_charred.png`

**Environment Assets (7 files):**
16. `env_forest_pristine.png`
17. `env_forest_floor.png`
18. `env_electrical_flash.png`
19. `env_log_explosion.png`
20. `env_crater_smoking.png`
21. `env_formation_ground.png`
22. `env_forest_edge.png`

**Total Assets:** 22 master seed images for Nano Bananao generation

---

This complete asset package is ready for Nano Bananao image generation, with each prompt optimized for the 5-second "breathing photograph" Kling AI workflow.

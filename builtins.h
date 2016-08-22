/**
  \file builtins.h
  \brief Built-in definitions for Nox Script
*/

typedef int any;
typedef int function;
typedef int object;
typedef int string;

/**
  \brief FALSE value
*/
const int FALSE = 0;
/**
  \brief TRUE value
*/
const int TRUE = 1;
/**
  \brief SELF object id

  This constant can be used any place where an object id is used.
*/
const int SELF = -1;
/**
  \brief OTHER object id

  This constant can be used any place where an object id is used.
*/
const int OTHER = -2;

/**
  \brief Audio events
*/
enum AudioEvent
{
    AnchorCast,
    AnchorOn,
    AnchorOff,
    BlindCast,
    BlindOn,
    BlindOff,
    BlinkCast,
    BurnCast,
    CleansingFlameCast,
    ChannelLifeCast,
    ChannelLifeEffect,
    ChannelLifeStop,
    CancelCast,
    CharmCast,
    CharmSuccess,
    CharmFailure,
    ConfuseCast,
    ConfuseOn,
    ConfuseOff,
    CounterspellCast,
    CurePoisonCast,
    CurePoisonEffect,
    DeathCast,
    DeathOn,
    DeathOff,
    DeathTimer,
    DeathRayCast,
    DetonateGlyphCast,
    DrainManaCast,
    EarthquakeCast,
    EnergyBoltCast,
    FearCast,
    FearOn,
    FearOff,
    ForceOfNatureCast,
    ForceOfNatureReflect,
    ForceOfNatureRelease,
    GlyphCast,
    GlyphDetonate,
    FireballCast,
    FireballExplode,
    FirewalkCast,
    FirewalkOn,
    FirewalkOff,
    FirewalkFlame,
    FistCast,
    FistHit,
    ForceFieldCast,
    FrostCast,
    FrostOn,
    FrostOff,
    FumbleCast,
    FumbleEffect,
    GreaterHealCast,
    GreaterHealEffect,
    GreaterHealStop,
    HasteCast,
    HasteOn,
    HasteOff,
    InfravisionCast,
    InfravisionOn,
    InfraVisionOff,
    InversionCast,
    InvisibilityCast,
    InvisibilityOn,
    InvisibilityOff,
    InvulnerabilityCast,
    InvulnerabilityOn,
    InvulnerabilityOff,
    InvulnerableEffect,
    LesserHealCast,
    LesserHealEffect,
    LightCast,
    LightOn,
    LightOff,
    LightningCast,
    LockCast,
    ManaBombCast,
    ManaBombEffect,
    MarkCast,
    MagicMissileCast,
    MagicMissileDetonate,
    MeteorCast,
    MeteorShowerCast,
    MeteorHit,
    MoonglowCast,
    MoonglowOn,
    MoonglowOff,
    NullifyCast,
    NullifyOn,
    NullifyOff,
    PhantomCast,
    PixieSwarmCast,
    PixieHit,
    PlasmaCast,
    PoisonCast,
    PoisonEffect,
    ProtectionFromFireCast,
    ProtectionFromFireOn,
    ProtectionFromFireOff,
    ProtectionFromFireEffect,
    ProtectionFromPoisonCast,
    ProtectionFromPoisonOn,
    ProtectionFromPoisonOff,
    ProtectionFromPoisonEffec,
    ProtectionFromElectricity,
    ProtectionFromElectricity,
    ProtectionFromElectricity,
    ProtectionFromElectricity,
    ProtectionFromMagicCast,
    ProtectionFromMagicOn,
    ProtectionFromMagicOff,
    ProtectionFromMagicEffect,
    PullCast,
    PushCast,
    ReflectiveShieldCast,
    ReflectiveShieldOn,
    ReflectiveShieldOff,
    ReflectiveShieldEffect,
    RegenerationOn,
    RegenerationOff,
    RunCast,
    RunOn,
    RunOff,
    ShieldCast,
    ShieldOn,
    ShieldOff,
    ShieldRepelled,
    ShockCast,
    ShockOn,
    ShockOff,
    Shocked,
    SlowCast,
    SlowOn,
    SlowOff,
    StunCast,
    StunOn,
    StunOff,
    SummonCast,
    SwapCast,
    TagCast,
    TagOn,
    TagOff,
    TeleportOut,
    TeleportIn,
    TeleportToMarkerCast,
    TeleportToMarkerEffect,
    TeleportPopCast,
    TeleportToTargetCast,
    TelekinesisCast,
    TelekinesisOn,
    TelekinesisOff,
    ToxicCloudCast,
    TriggerGlyphCast,
    TurnUndeadCast,
    TurnUndeadEffect,
    VampirismCast,
    VampirismOn,
    VampirismOff,
    DrainHealth,
    VillainCast,
    VillainOn,
    VillainOff,
    WallCast,
    WallOn,
    WallOff,
    BerserkerChargeInvoke,
    BerserkerCrash,
    BerserkerChargeOn,
    BerserkerChargeOff,
    WarcryInvoke,
    WarcryOn,
    WarcryOff,
    HarpoonInvoke,
    HarpoonOn,
    HarpoonOff,
    TreadLightlyInvoke,
    TreadLightlyOn,
    TreadLightlyOff,
    EyeOfTheWolfInvoke,
    EyeOfTheWolfOn,
    EyeOfTheWolfOff,
    SpellPhonemeUp,
    SpellPhonemeUpRight,
    SpellPhonemeRight,
    SpellPhonemeDownRight,
    SpellPhonemeDown,
    SpellPhonemeDownLeft,
    SpellPhonemeLeft,
    SpellPhonemeUpLeft,
    FemaleSpellPhonemeUp,
    FemaleSpellPhonemeUpRight,
    FemaleSpellPhonemeRight,
    FemaleSpellPhonemeDownRig,
    FemaleSpellPhonemeDown,
    FemaleSpellPhonemeDownLef,
    FemaleSpellPhonemeLeft,
    FemaleSpellPhonemeUpLeft,
    NPCSpellPhonemeUp,
    NPCSpellPhonemeUpRight,
    NPCSpellPhonemeRight,
    NPCSpellPhonemeDownRight,
    NPCSpellPhonemeDown,
    NPCSpellPhonemeDownLeft,
    NPCSpellPhonemeLeft,
    NPCSpellPhonemeUpLeft,
    NPCFemaleSpellPhonemeUp,
    NPCFemaleSpellPhonemeUpRi,
    NPCFemaleSpellPhonemeRigh,
    NPCFemaleSpellPhonemeDown,
    NPCFemaleSpellPhonemeDown,
    NPCFemaleSpellPhonemeDown,
    NPCFemaleSpellPhonemeLeft,
    NPCFemaleSpellPhonemeUpLe,
    FireballWand,
    SmallFireballWand,
    FlareWand,
    LightningWand,
    DepletedWand,
    Ricochet,
    WeaponEffectFire,
    WeaponEffectElectricity,
    PermanentFizzle,
    ManaEmpty,
    Lock,
    Unlock,
    ElevEnable,
    ElevDisable,
    OpenWoodenDoor,
    MoveWoodenDoor,
    CloseWoodenDoor,
    WoodenDoorLocked,
    OpenGate,
    MoveGate,
    CloseGate,
    GateLocked,
    OpenWoodenGate,
    CloseWoodenGate,
    OpenHeavyWoodenDoor,
    CloseHeavyWoodenDoor,
    ElevStoneUp,
    ElevStoneDown,
    ElevWoodUp,
    ElevWoodDown,
    ElevMechUp,
    ElevMechDown,
    ElevLavaUp,
    ElevLavaDown,
    ElevGreenUp,
    ElevGreenDown,
    ElevLOTDUp,
    ElevLOTDDown,
    Gear1,
    Gear2,
    Gear3,
    SmallRockMove,
    MediumRockMove,
    LargeRockMove,
    BoulderMove,
    WalkOnSnow,
    WalkOnStone,
    WalkOnDirt,
    WalkOnWood,
    WalkOnWater,
    WalkOnMud,
    RunOnSnow,
    RunOnStone,
    RunOnDirt,
    RunOnWood,
    RunOnWater,
    RunOnMud,
    PlayerFallThud,
    BarrelMove,
    BlackPowderBurn,
    FireExtinguish,
    PolypExplode,
    PowderBarrelExplode,
    BarrelBreak,
    WaterBarrelBreak,
    LOTDBarrelBreak,
    WineCaskBreak,
    BarrelStackBreak,
    CoffinBreak,
    WaspHiveBreak,
    WorkstationBreak,
    CrushLight,
    CrushMedium,
    CrushHard,
    SentryRayHitWall,
    SentryRayHit,
    DeathRayKill,
    TauntLaugh,
    TauntShakeFist,
    TauntPoint,
    FlagPickup,
    FlagDrop,
    FlagRespawn,
    FlagCapture,
    TreasurePickup,
    TreasureDrop,
    GameOver,
    ServerOptionsChange,
    CamperAlarm,
    PlayerEliminated,
    CrownChange,
    HumanMaleEatFood,
    HumanMaleEatApple,
    HumanMaleDrinkJug,
    HumanMaleHurtLight,
    HumanMaleHurtMedium,
    HumanMaleHurtHeavy,
    HumanMaleHurtPoison,
    HumanMaleDie,
    HumanMaleExertionLight,
    HumanMaleExertionHeavy,
    HumanFemaleEatFood,
    HumanFemaleEatApple,
    HumanFemaleDrinkJug,
    HumanFemaleHurtLight,
    HumanFemaleHurtMedium,
    HumanFemaleHurtHeavy,
    HumanFemaleHurtPoison,
    HumanFemaleDie,
    HumanFemaleExertionLight,
    HumanFemaleExertionHeavy,
    MonsterEatFood,
    BatMove,
    BatRecognize,
    BatBite,
    BatDie,
    SmallSpiderMove,
    SmallSpiderIdle,
    SmallSpiderRecognize,
    SmallSpiderBite,
    SmallSpiderDie,
    LargeSpiderMove,
    LargeSpiderIdle,
    LargeSpiderRecognize,
    LargeSpiderBite,
    LargeSpiderSpit,
    WebGooHit,
    LargeSpiderDie,
    SkeletonMove,
    SkeletonRecognize,
    SkeletonHitting,
    SkeletonMissing,
    SkeletonAttackInit,
    SkeletonDie,
    SkeletonLordMove,
    SkeletonLordRecognize,
    SkeletonLordHitting,
    SkeletonLordMissing,
    SkeletonLordAttackInit,
    SkeletonLordDie,
    BomberRecognize,
    BomberSummon,
    BomberMove,
    BomberDie,
    DemonRecognize,
    DemonTaunt,
    DemonSpellInit,
    DemonMove,
    DemonHurt,
    DemonDie,
    GruntTaunt,
    GruntIdle,
    GruntBowTwang,
    GruntRecognize,
    GruntMove,
    GruntAttackInit,
    GruntHitting,
    GruntMissing,
    GruntHurt,
    GruntDie,
    OgreBruteTaunt,
    OgreBruteIdle,
    OgreBruteListen,
    OgreBruteAttackInit,
    OgreBruteMeleeMiss,
    OgreBruteEngage,
    OgreBruteRecognize,
    OgreBruteMove,
    OgreBruteHurt,
    OgreBruteMeleeHit,
    OgreBruteDie,
    OgreWarlordTaunt,
    OgreWarlordIdle,
    OgreWarlordListen,
    OgreWarlordAttackInit,
    OgreWarlordMeleeMiss,
    OgreWarlordEngage,
    OgreWarlordRecognize,
    OgreWarlordThrow,
    OgreWarlordMove,
    OgreWarlordHurt,
    OgreWarlordMeleeHit,
    OgreWarlordDie,
    ScorpionMove,
    ScorpionIdle,
    ScorpionRecognize,
    ScorpionStingHit,
    ScorpionStingMiss,
    ScorpionAttackInit,
    ScorpionHurt,
    ScorpionDie,
    LeechMove,
    LeechIdle,
    LeechRecognize,
    LeechHitting,
    LeechMissing,
    LeechAttackInit,
    LeechHurt,
    LeechDie,
    ZombieMove,
    ZombieIdle,
    ZombieRecognize,
    ZombieHitting,
    ZombieMissing,
    ZombieAttackInit,
    ZombieHurt,
    ZombieDie,
    VileZombieMove,
    VileZombieIdle,
    VileZombieRecognize,
    VileZombieHitting,
    VileZombieMissing,
    VileZombieAttackInit,
    VileZombieHurt,
    VileZombieDie,
    BearMove,
    BearRecognize,
    BearHitting,
    BearMissing,
    BearAttackInit,
    BearHurt,
    BearDie,
    WolfMove,
    WolfIdle,
    WolfRecognize,
    WolfHitting,
    WolfMissing,
    WolfAttackInit,
    WolfHurt,
    WolfDie,
    PlantRecognize,
    PlantHitting,
    PlantMissing,
    PlantAttackInit,
    PlantHurt,
    PlantDie,
    MimicMove,
    MimicIdle,
    MimicRecognize,
    MimicAttackInit,
    MimicHitting,
    MimicMissing,
    MimicHurt,
    MimicDie,
    MechGolemRecognize,
    MechGolemHitting,
    MechGolemMissing,
    MechGolemMove,
    MechGolemAttackInit,
    MechGolemHurt,
    MechGolemDie,
    ImpMove,
    ImpRecognize,
    ImpSteal,
    ImpShoot,
    ImpDie,
    GolemRecognize,
    GolemMove,
    GolemHitting,
    GolemMissing,
    GolemHurt,
    GolemDie,
    TowerRecognize,
    TowerShoot,
    SkullRecognize,
    SkullShoot,
    GhostMove,
    GhostRecognize,
    GhostHitting,
    GhostHurt,
    GhostDie,
    WizardTalkable,
    WizardMove,
    WizardRecognize,
    WizardEngage,
    WizardRetreat,
    WizardHurt,
    WizardDie,
    WaspMove,
    WaspIdle,
    WaspRecognize,
    WaspSting,
    WaspDie,
    EmberDemonMove,
    EmberDemonTaunt,
    EmberDemonRecognize,
    EmberDemonHitting,
    EmberDemonMissing,
    EmberDemonThrow,
    EmberDemonHurt,
    EmberDemonDie,
    UrchinMove,
    UrchinTaunt,
    UrchinIdle,
    UrchinRecognize,
    UrchinThrow,
    UrchinHurt,
    UrchinFlee,
    UrchinDie,
    UrchinShamanMove,
    UrchinShamanTaunt,
    UrchinShamanIdle,
    UrchinShamanRecognize,
    UrchinShamanHurt,
    UrchinShamanFlee,
    UrchinShamanDie,
    ArcherMove,
    ArcherTaunt,
    ArcherIdle,
    ArcherRetreat,
    ArcherRecognize,
    ArcherMissileInit,
    ArcherShoot,
    ArcherHurt,
    ArcherDie,
    SwordsmanMove,
    SwordsmanTaunt,
    SwordsmanIdle,
    SwordsmanRecognize,
    SwordsmanHitting,
    SwordsmanMissing,
    SwordsmanRetreat,
    SwordsmanAttackInit,
    SwordsmanHurt,
    SwordsmanDie,
    BeholderMove,
    BeholderIdle,
    BeholderRecognize,
    BeholderAttackInit,
    BeholderHurt,
    BeholderDie,
    DryadMove,
    DryadTaunt,
    DryadRecognize,
    DryadHurt,
    DryadDie,
    EvilCherubMove,
    EvilCherubTaunt,
    EvilCherubIdle,
    EvilCherubMissileInit,
    EvilCherubRecognize,
    EvilCherubShoot,
    EvilCherubHurt,
    EvilCherubDie,
    FishDie,
    FrogDie,
    FrogRecognize,
    HecubahTaunt,
    HecubahTalkable,
    HecubahMove,
    HecubahRecognize,
    HecubahAttackInit,
    HecubahHurt,
    HecubahDie,
    HecubahDieFrame0A,
    HecubahDieFrame0B,
    HecubahDieFrame98,
    HecubahDieFrame194,
    HecubahDieFrame283,
    HecubahDieFrame439,
    NecromancerTaunt,
    NecromancerTalkable,
    NecromancerMove,
    NecromancerRecognize,
    NecromancerEngage,
    NecromancerRetreat,
    NecromancerAttackInit,
    NecromancerHurt,
    NecromancerDie,
    LichMove,
    LichRecognize,
    LichAttackInit,
    LichHurt,
    LichDie,
    FlyingGolemMove,
    FlyingGolemRecognize,
    FlyingGolemShoot,
    FlyingGolemHurt,
    FlyingGolemDie,
    NPCIdle,
    NPCTalkable,
    NPCRecognize,
    NPCRetreat,
    NPCHurt,
    NPCDie,
    MaidenIdle,
    MaidenTalkable,
    MaidenFlee,
    MaidenHurt,
    MaidenDie,
    RatDie,
    ShadeMove,
    ShadeRecognize,
    ShadeAttackInit,
    ShadeHurt,
    ShadeDie,
    WeirdlingMove,
    WillOWispMove,
    WillOWispIdle,
    WillOWispRecognize,
    WillOWispEngage,
    WillOWispHurt,
    WillOWispDie,
    TrollMove,
    TrollIdle,
    TrollRecognize,
    TrollHurt,
    TrollAttackInit,
    TrollFlatus,
    TrollDie,
    MaleNPC1Idle,
    MaleNPC1Talkable,
    MaleNPC1Recognize,
    MaleNPC1Engage,
    MaleNPC1Retreat,
    MaleNPC1Hurt,
    MaleNPC1AttackInit,
    MaleNPC1Die,
    MaleNPC2Idle,
    MaleNPC2Talkable,
    MaleNPC2Recognize,
    MaleNPC2Engage,
    MaleNPC2Retreat,
    MaleNPC2Hurt,
    MaleNPC2AttackInit,
    MaleNPC2Die,
    Maiden1Talkable,
    Maiden1Idle,
    Maiden1Recognize,
    Maiden1Retreat,
    Maiden1Hurt,
    Maiden1AttackInit,
    Maiden1Die,
    Maiden2Idle,
    Maiden2Talkable,
    Maiden2Recognize,
    Maiden2Retreat,
    Maiden2Hurt,
    Maiden2AttackInit,
    Maiden2Die,
    HorvathTalkable,
    HorvathEngage,
    HorvathHurt,
    HorvathDie,
    Wizard1Idle,
    Wizard1Talkable,
    Wizard1Recognize,
    Wizard1Engage,
    Wizard1Retreat,
    Wizard1Hurt,
    Wizard1AttackInit,
    Wizard1Die,
    Wizard2Idle,
    Wizard2Talkable,
    Wizard2Recognize,
    Wizard2Engage,
    Wizard2Retreat,
    Wizard2Hurt,
    Wizard2AttackInit,
    Wizard2Die,
    FireKnight1Idle,
    FireKnight1Talkable,
    FireKnight1Recognize,
    FireKnight1Engage,
    FireKnight1Retreat,
    FireKnight1Hurt,
    FireKnight1AttackInit,
    FireKnight1Die,
    FireKnight2Idle,
    FireKnight2Talkable,
    FireKnight2Recognize,
    FireKnight2Engage,
    FireKnight2Retreat,
    FireKnight2Hurt,
    FireKnight2AttackInit,
    FireKnight2Die,
    Guard1Idle,
    Guard1Talkable,
    Guard1Recognize,
    Guard1Engage,
    Guard1Retreat,
    Guard1Hurt,
    Guard1AttackInit,
    Guard1Die,
    Guard2Idle,
    Guard2Talkable,
    Guard2Recognize,
    Guard2Engage,
    Guard2Retreat,
    Guard2Hurt,
    Guard2AttackInit,
    Guard2Die,
    WoundedNPCIdle,
    WoundedNPCTalkable,
    WoundedNPCRecognize,
    WoundedNPCRetreat,
    WoundedNPCHurt,
    WoundedNPCAttackInit,
    WoundedNPCDie,
    HorrendousTalkable,
    HorrendousRecognize,
    HorrendousRetreat,
    HorrendousHurt,
    HorrendousAttackInit,
    HorrendousDie,
    PotionUse,
    RestoreHealth,
    RestoreMana,
    SecretWallOpen,
    SecretWallClose,
    SecretWallEarthOpen,
    SecretWallEarthClose,
    SecretWallMetalOpen,
    SecretWallMetalClose,
    SecretWallStoneOpen,
    SecretWallStoneClose,
    SecretWallWoodOpen,
    SecretWallWoodClose,
    TriggerPressed,
    TriggerReleased,
    PotionBreak,
    WallDestroyed,
    WallDestroyedStone,
    WallDestroyedWood,
    WallDestroyedMetal,
    ChestOpen,
    CryptChestOpen,
    SackChestOpen,
    EggBreak,
    ButtonPress,
    ButtonRelease,
    LeverToggle,
    SwitchToggle,
    ChainPull,
    ShortBellsUp,
    LongBellsUp,
    LongBellsDown,
    BigBell,
    MetallicBong,
    Chime,
    BigGong,
    SmallGong,
    MysticChant,
    TripleChime,
    Clank1,
    Clank2,
    Clank3,
    MapOpen,
    MapClose,
    BookOpen,
    BookClose,
    PageTurn,
    InventoryOpen,
    InventoryClose,
    InventoryPickup,
    InventoryDrop,
    SpellPickup,
    SpellDrop,
    SpellPopOffBook,
    TrapEditorOpen,
    TrapEditorClose,
    ChangeSpellbar,
    ExpandSpellbar,
    CollapseSpellbar,
    CreatureCageAppears,
    CreatureCageHides,
    ShopRepairItem,
    MetalArmorPickup,
    MetalArmorDrop,
    MetalArmorBreak,
    LeatherArmorPickup,
    LeatherArmorDrop,
    LeatherArmorBreak,
    WoodenArmorPickup,
    WoodenArmorDrop,
    WoodenArmorBreak,
    ClothArmorPickup,
    ClothArmorDrop,
    ClothArmorBreak,
    ShoesPickup,
    ShoesDrop,
    MetalWeaponBreak,
    WoodWeaponBreak,
    KeyPickup,
    KeyDrop,
    AmuletPickup,
    AmuletDrop,
    TrapPickup,
    TrapDrop,
    BookPickup,
    BookDrop,
    ScrollPickup,
    ScrollDrop,
    WandPickup,
    WandDrop,
    PotionPickup,
    PotionDrop,
    MeatPickup,
    MeatDrop,
    ApplePickup,
    AppleDrop,
    ShroomPickup,
    ShroomDrop,
    SpectaclesPickup,
    SpectaclesDrop,
    MetalWeaponPickup,
    WoodenWeaponPickup,
    MetalWeaponDrop,
    WoodenWeaponDrop,
    BearTrapTriggered,
    PoisonTrapTriggered,
    StoneHitStone,
    StoneHitEarth,
    StoneHitWood,
    StoneHitMetal,
    StoneHitFlesh,
    WoodHitStone,
    WoodHitEarth,
    WoodHitWood,
    WoodHitMetal,
    WoodHitFlesh,
    MetalHitStone,
    MetalHitEarth,
    MetalHitWood,
    MetalHitMetal,
    MetalHitFlesh,
    FleshHitStone,
    FleshHitEarth,
    FleshHitWood,
    FleshHitMetal,
    FleshHitFlesh,
    DiamondHitStone,
    DiamondHitEarth,
    DiamondHitWood,
    DiamondHitMetal,
    DiamondHitFlesh,
    HitStoneBreakable,
    HitEarthBreakable,
    HitWoodBreakable,
    HitMetalBreakable,
    HitMagicBreakable,
    HitMetalShield,
    PunchMissing,
    LongswordMissing,
    SwordMissing,
    HammerMissing,
    AxeMissing,
    MaceMissing,
    BowEmpty,
    CrossBowEmpty,
    BowShoot,
    CrossBowShoot,
    ArrowTrapShoot,
    GreatSwordReflect,
    ChakramThrow,
    ChakramCatch,
    ChakramFallToGround,
    StaffBlock,
    NextWeapon,
    HeartBeat,
    GenerateTick,
    SummonClick,
    SummonComplete,
    SummonAbort,
    ManaClick,
    LevelUp,
    JournalEntryAdd,
    SecretFound,
    EarthRumbleMajor,
    EarthRumbleMinor,
    ElectricalArc1,
    FloorSpikesUp,
    FloorSpikesDown,
    SpikeBlockMove,
    BoulderRoll,
    ArcheryContestBegins,
    HorrendousIsKilled,
    StaffOblivionAchieve1,
    StaffOblivionAchieve2,
    StaffOblivionAchieve3,
    StaffOblivionAchieve4,
    FireGrate,
    MechGolemPowerUp,
    ShellSelect,
    ShellClick,
    ShellSlideIn,
    ShellSlideOut,
    ShellMouseBoom,
    NoCanDo,
    BallThrow,
    BallGrab,
    BallBounce,
    BallHitGoal,
    HarpoonBroken,
    HarpoonReel,
    MonsterGeneratorDie,
    MonsterGeneratorHurt,
    MonsterGeneratorSpawn,
    PlayerExit,
    AwardLife,
    SoulGateTouch,
    QuestRespawn,
    QuestFinalDeath,
    QuestPlayerJoinGame,
    QuestStatScreen,
    QuestIntroScreen,
    QuestPlayerExitGame,
    QuestLockedChest,
    StoneDoorOpen,
    StoneDoorClose,
    DiamondPickup,
    DiamondDrop,
    EnableSharedKeyMode,
};

/**
  \brief Class names
*/
enum Class
{
    MISSILE,
    MONSTER,
    PLAYER,
    OBSTACLE,
    FOOD,
    EXIT,
    KEY,
    DOOR,
    INFO_BOOK,
    TRIGGER,
    TRANSPORTER,
    HOLE,
    WAND,
    FIRE,
    ELEVATOR,
    ELEVATOR_SHAFT,
    DANGEROUS,
    MONSTERGENERATOR,
    READABLE,
    LIGHT,
    SIMPLE,
    COMPLEX,
    IMMOBILE,
    VISIBLE_ENABLE,
    WEAPON,
    ARMOR,
    NOT_STACKABLE,
    TREASURE,
    FLAG,
    CLIENT_PERSIST,
    CLIENT_PREDICT,
    PICKUP
};

/**
  \brief Damange types
*/
enum DamageType
{
    DAMAGE_BLADE = 0,
    DAMAGE_FLAME = 1,
    DAMAGE_CRUSH = 2,
    DAMAGE_IMPALE = 3,
    DAMAGE_DRAIN = 4,
    DAMAGE_POISON = 5,
    DAMAGE_DISPEL_UNDEAD = 6,
    DAMAGE_EXPLOSION = 7,
    DAMAGE_BITE = 8,
    DAMAGE_ELECTRIC = 9,
    DAMAGE_CLAW = 10,
    DAMAGE_IMPACT = 11,
    DAMAGE_LAVA = 12,
    DAMAGE_DEATH_MAGIC = 13,
    DAMAGE_PLASMA = 14,
    DAMAGE_MANA_BOMB = 15,
    DAMAGE_ZAP_RAY = 16,
    DAMAGE_AIRBORNE_ELECTRIC = 17,
};

/**
  \brief Effects
*/
enum Effect
{
    PARTICLEFX,
    PLASMA,
    SUMMON,
    SUMMON_CANCEL,
    SHIELD,
    BLUE_SPARKS,
    YELLOW_SPARKS,
    CYAN_SPARKS,
    VIOLET_SPARKS,
    EXPLOSION,
    LESSER_EXPLOSION,
    COUNTERSPELL_EXPLOSION,
    THIN_EXPLOSION,
    TELEPORT,
    SMOKE_BLAST,
    DAMAGE_POOF,
    LIGHTNING,
    ENERGY_BOLT,
    CHAIN_LIGHTNING_BOLT,
    DRAIN_MANA,
    CHARM,
    GREATER_HEAL,
    MAGIC,
    SPARK_EXPLOSION,
    DEATH_RAY,
    SENTRY_RAY,
    RICOCHET,
    JIGGLE,
    GREEN_BOLT,
    GREEN_EXPLOSION,
    WHITE_FLASH,
    GENERATING_MAP,
    ASSEMBLING_MAP,
    POPULATING_MAP,
    DURATION_SPELL,
    DELTAZ_SPELL_START,
    TURN_UNDEAD,
    ARROW_TRAP,
    VAMPIRISM,
    MANA_BOMB_CANCEL,
};

/**
  \brief Enchants
*/
enum Enchant
{
    ENCHANT_INVISIBLE,
    ENCHANT_MOONGLOW,
    ENCHANT_BLINDED,
    ENCHANT_CONFUSED,
    ENCHANT_SLOWED,
    ENCHANT_HELD,
    ENCHANT_DETECTING,
    ENCHANT_ETHEREAL,
    ENCHANT_RUN,
    ENCHANT_HASTED,
    ENCHANT_VILLAIN,
    ENCHANT_AFRAID,
    ENCHANT_BURNING,
    ENCHANT_VAMPIRISM,
    ENCHANT_ANCHORED,
    ENCHANT_LIGHT,
    ENCHANT_DEATH,
    ENCHANT_PROTECT_FROM_FIRE,
    ENCHANT_PROTECT_FROM_POISON,
    ENCHANT_PROTECT_FROM_MAGIC,
    ENCHANT_PROTECT_FROM_ELECTRICITY,
    ENCHANT_INFRAVISION,
    ENCHANT_SHOCK,
    ENCHANT_INVULNERABLE,
    ENCHANT_TELEKINESIS,
    ENCHANT_FREEZE,
    ENCHANT_SHIELD,
    ENCHANT_REFLECTIVE_SHIELD,
    ENCHANT_CHARMING,
    ENCHANT_ANTI_MAGIC,
    ENCHANT_CROWN,
    ENCHANT_SNEAK
};

/**
  \brief Facing directions
*/
enum Direction
{
    NW = 0,
    N = 1,
    NE = 2,
    W = 3,
    E = 5,
    SW = 6,
    S = 7,
    SE = 8
};

/**
  \brief Spell names
*/
enum Spell
{
    SPELL_INVALID,
    SPELL_ANCHOR,
    SPELL_ARACHNAPHOBIA,
    SPELL_BLIND,
    SPELL_BLINK,
    SPELL_BURN,
    SPELL_CANCEL,
    SPELL_CHAIN_LIGHTNING_BOLT,
    SPELL_CHANNEL_LIFE,
    SPELL_CHARM,
    SPELL_CLEANSING_FLAME,
    SPELL_CLEANSING_MANA_FLAME,
    SPELL_CONFUSE,
    SPELL_COUNTERSPELL,
    SPELL_CURE_POISON,
    SPELL_DEATH,
    SPELL_DEATH_RAY,
    SPELL_DETECT_MAGIC,
    SPELL_DETONATE,
    SPELL_DETONATE_GLYPHS,
    SPELL_DISENCHANT_ALL,
    SPELL_TURN_UNDEAD,
    SPELL_DRAIN_MANA,
    SPELL_EARTHQUAKE,
    SPELL_LIGHTNING,
    SPELL_EXPLOSION,
    SPELL_FEAR,
    SPELL_FIREBALL,
    SPELL_FIREWALK,
    SPELL_FIST,
    SPELL_FORCE_FIELD,
    SPELL_FORCE_OF_NATURE,
    SPELL_FREEZE,
    SPELL_FUMBLE,
    SPELL_GLYPH,
    SPELL_GREATER_HEAL,
    SPELL_HASTE,
    SPELL_INFRAVISION,
    SPELL_INVERSION,
    SPELL_INVISIBILITY,
    SPELL_INVULNERABILITY,
    SPELL_LESSER_HEAL,
    SPELL_LIGHT,
    SPELL_CHAIN_LIGHTNING,
    SPELL_LOCK,
    SPELL_MARK,
    SPELL_MARK_1,
    SPELL_MARK_2,
    SPELL_MARK_3,
    SPELL_MARK_4,
    SPELL_MAGIC_MISSILE,
    SPELL_SHIELD,
    SPELL_METEOR,
    SPELL_METEOR_SHOWER,
    SPELL_MOONGLOW,
    SPELL_NULLIFY,
    SPELL_MANA_BOMB,
    SPELL_PHANTOM,
    SPELL_PIXIE_SWARM,
    SPELL_PLASMA,
    SPELL_POISON,
    SPELL_PROTECTION_FROM_ELECTRICITY,
    SPELL_PROTECTION_FROM_FIRE,
    SPELL_PROTECTION_FROM_MAGIC,
    SPELL_PROTECTION_FROM_POISON,
    SPELL_PULL,
    SPELL_PUSH,
    SPELL_OVAL_SHIELD,
    SPELL_RESTORE_HEALTH,
    SPELL_RESTORE_MANA,
    SPELL_RUN,
    SPELL_SHOCK,
    SPELL_SLOW,
    SPELL_SMALL_ZAP,
    SPELL_STUN,
    SPELL_SUMMON_BAT,
    SPELL_SUMMON_BLACK_BEAR,
    SPELL_SUMMON_BEAR,
    SPELL_SUMMON_BEHOLDER,
    SPELL_SUMMON_BOMBER,
    SPELL_SUMMON_CARNIVOROUS_PLANT,
    SPELL_SUMMON_ALBINO_SPIDER,
    SPELL_SUMMON_SMALL_ALBINO_SPIDER,
    SPELL_SUMMON_EVIL_CHERUB,
    SPELL_SUMMON_EMBER_DEMON,
    SPELL_SUMMON_GHOST,
    SPELL_SUMMON_GIANT_LEECH,
    SPELL_SUMMON_IMP,
    SPELL_SUMMON_MECHANICAL_FLYER,
    SPELL_SUMMON_MECHANICAL_GOLEM,
    SPELL_SUMMON_MIMIC,
    SPELL_SUMMON_OGRE,
    SPELL_SUMMON_OGRE_BRUTE,
    SPELL_SUMMON_OGRE_WARLORD,
    SPELL_SUMMON_SCORPION,
    SPELL_SUMMON_SHADE,
    SPELL_SUMMON_SKELETON,
    SPELL_SUMMON_SKELETON_LORD,
    SPELL_SUMMON_SPIDER,
    SPELL_SUMMON_SMALL_SPIDER,
    SPELL_SUMMON_SPITTING_SPIDER,
    SPELL_SUMMON_STONE_GOLEM,
    SPELL_SUMMON_TROLL,
    SPELL_SUMMON_URCHIN,
    SPELL_SUMMON_WASP,
    SPELL_SUMMON_WILLOWISP,
    SPELL_SUMMON_WOLF,
    SPELL_SUMMON_BLACK_WOLF,
    SPELL_SUMMON_WHITE_WOLF,
    SPELL_SUMMON_ZOMBIE,
    SPELL_SUMMON_VILE_ZOMBIE,
    SPELL_SUMMON_DEMON,
    SPELL_SUMMON_LICH,
    SPELL_SUMMON_DRYAD,
    SPELL_SUMMON_URCHIN_SHAMAN,
    SPELL_SWAP,
    SPELL_TAG,
    SPELL_TELEPORT_OTHER_TO_MARK_1,
    SPELL_TELEPORT_OTHER_TO_MARK_2,
    SPELL_TELEPORT_OTHER_TO_MARK_3,
    SPELL_TELEPORT_OTHER_TO_MARK_4,
    SPELL_TELEPORT_POP,
    SPELL_TELEPORT_TO_MARK_1,
    SPELL_TELEPORT_TO_MARK_2,
    SPELL_TELEPORT_TO_MARK_3,
    SPELL_TELEPORT_TO_MARK_4,
    SPELL_TELEPORT_TO_TARGET,
    SPELL_TELEKINESIS,
    SPELL_TOXIC_CLOUD,
    SPELL_TRIGGER_GLYPH,
    SPELL_VAMPIRISM,
    SPELL_VILLAIN,
    SPELL_WALL,
    SPELL_WINK,
    SPELL_SUMMON_CREATURE,
    SPELL_MARK_LOCATION,
    SPELL_TELEPORT_TO_MARKER
};

/**
  \brief Subclass names
*/
enum Subclass
{
    HELMET,
    SHIELD,
    BREASTPLATE,
    ARM_ARMOR,
    PANTS,
    BOOTS,
    SHIRT,
    LEG_ARMOR,
    BACK,
    FLAG,
    QUIVER,
    CROSSBOW,
    ARROW,
    BOLT,
    CHAKRAM,
    SHURIKEN,
    SWORD,
    LONG_SWORD,
    GREAT_SWORD,
    MACE,
    OGRE_AXE,
    HAMMER,
    STAFF,
    STAFF_SULPHOROUS_FLARE,
    STAFF_SULPHOROUS_SHOWER,
    STAFF_LIGHTNING,
    STAFF_FIREBALL,
    STAFF_TRIPLE_FIREBALL,
    STAFF_FORCE_OF_NATURE,
    STAFF_DEATH_RAY,
    STAFF_OBLIVION_HALBERD,
    STAFF_OBLIVION_HEART,
    STAFF_OBLIVION_WIERDLING,
    STAFF_OBLIVION_ORB,
    SMALL_MONSTER,
    MEDIUM_MONSTER,
    LARGE_MONSTER,
    SHOPKEEPER,
    NPC,
    FEMALE_NPC,
    UNDEAD,
    MONITOR,
    MIGRATE,
    IMMUNE_POISON,
    IMMUNE_FIRE,
    IMMUNE_ELECTRICITY,
    IMMUNE_FEAR,
    BOMBER,
    NO_TARGET,
    NO_SPELL_TARGET,
    HAS_SOUL,
    WARCRY_STUN,
    LOOK_AROUND,
    WOUNDED_NPC,
    SIMPLE,
    APPLE,
    POTION,
    HEALTH_POTION,
    MANA_POTION,
    CURE_POISON_POTION,
    MUSHROOM,
    HASTE_POTION,
    INVISIBILITY_POTION,
    SHIELD_POTION,
    FIRE_PROTECT_POTION,
    SHOCK_PROTECT_POTION,
    POISON_PROTECT_POTION,
    INVULNERABILITY_POTION,
    INFRAVISION_POTION,
    VAMPIRISM_POTION,
    HEAVY,
    LAVA,
    GATE,
    VISIBLE_OBELISK,
    INVISIBLE_OBELISK,
    TECH,
    LOTD,
    USEABLE,
    CHEST_NW,
    CHEST_NE,
    CHEST_SE,
    CHEST_SW,
    STONE_DOOR,
    SPELL_BOOK,
    FIELD_GUIDE,
    ABILITY_BOOK,
    MISSILE_COUNTERSPELL,
    MAGIC,
    GENERATOR_NW,
    GENERATOR_NE,
    GENERATOR_SE,
    GENERATOR_SW,
    QUEST_EXIT,
    QUEST_WARP_EXIT,
    FLESH,
    CLOTH,
    ANIMAL_HIDE,
    WOOD,
    METAL,
    STONE,
    EARTH,
    LIQUID,
    GLASS,
    PAPER,
    SNOW,
    MUD,
    MAGIC,
    DIAMOND,
    NONE,
};

/**
  \brief Get a pointer to a wall by its wall coordinates.

  \param x wall coordinate X
  \param y wall coordinate Y
  \return wall object
*/
object Wall(int x, int y);

/**
  \brief Open a wall.

  \param wall a wall object
*/
void WallOpen(object wall);

/**
  \brief Open walls in a group.

  \param wallGroup a wall group object
*/
void WallGroupOpen(object wallGroup);

/**
  \brief Close a wall.

  \param wall a wall object
*/
void WallClose(object wall);

/**
  \brief Close walls in a group.

  \param wallGroup a wall group object
*/
void WallGroupClose(object wallGroup);

/**
  \brief Toggle a wall.

  This will toggle wall between opened and closed.

  \param wall a wall object
*/
void WallToggle(object wall);

/**
  \brief Toggle walls in a group.

  This will toggle a wall group between opened and closed.

  \param wallGroup a wall group object
*/
void WallGroupToggle(object wallGroup);

/**
  \brief Breaks a wall.

  This will break a wall. The wall must be breakable.

  \param wall a wall object
*/
void WallBreak(object wall);

/**
  \brief Breaks walls in a group.

  This will break walls in a group. The walls must be breakable.

  \param wallGroup a wall group object
*/
void WallGroupBreak(object wallGroup);

/**
  \brief Create a timer with delay in seconds.

  This will create a timer that calls the given script function after a
  delay given in seconds.

  \param seconds delay
  \param callback a script function
  \return timer id
*/
int SecondTimer(int seconds, function callback);

/**
  \brief Create a timer with delay in frames.

  This will create a timer that calls the given script function after a
  delay given in frames.

  \param frames delay
  \param callback a script function
  \return timer id
*/
int FrameTimer(int frames, function callback);

/**
  \brief Move an object to a waypoint.

  This moves an object to a waypoint. The object must be movable or attached
  to a "Mover". If the waypoint is linked, the object will continue to move
  once it reaches the first waypoint.

  \param id an object id
  \param waypoint a waypoint object
*/
void Move(int id, object waypoint);

/**
  \brief Move objects in a group to a waypoint.

  This moves the objects in a group to a waypoint. The objects must be movable
  or attached to a "Mover". If the waypoint is linked, the objects will
  continue to move once they reach the first waypoint.

  \param objectGroup an object group object
  \param waypoint a waypoint object
*/
void GroupMove(object objectGroup, object waypoint);

/**
  \brief Cause object to look in a direction.

  \param id an object id
  \param direction see ::Direction
*/
void LookAtDirection(int id, int direction);

/**
  \brief Cause objects in a group to look in a direction.

  \param objectGroup an object group object
  \param direction see ::Direction
*/
void GroupLookAtDirection(object objectGroup, int direction);

/**
  \brief Enable an object.

  \param id an object id
*/
void ObjectOn(int id);

/**
  \brief Enable objects in a group.

  \param objectGroup an object group object
*/
void ObjectGroupOn(object objectGroup);

/**
  \brief Enable a waypoint.

  \param waypoint a waypoint object
*/
void WayPointOn(object waypoint);

/**
  \brief Enable waypoints in a group.

  \param waypointGroup a waypoint group object
*/
void WayPointGroupOn(object waypointGroup);

/**
  \brief Disable an object.

  \param id an object id
*/
void ObjectOff(int id);

/**
  \brief Disable objects in a group.

  \param objectGroup an object group object
*/
void ObjectGroupOff(object objectGroup);

/**
  \brief Disable a waypoint.

  \param waypoint a waypoint object
*/
void WayPointOff(object waypoint);

/**
  \brief Disable waypoints in a group.

  \param waypointGroup a waypoint group object
*/
void WayPointGroupOff(object waypointGroup);

/**
  \brief Toggle whether object is disabled.

  \param id an object id
*/
void ObjectToggle(int id);

/**
  \brief Toggle whether objects in group are disabled.

  \param objectGroup an object group object
*/
void ObjectGroupToggle(object objectGroup);

/**
  \brief Toggle whether waypoint is disabled.

  \param waypoint a waypoint object
*/
void WayPointToggle(object waypoint);

/**
  \brief Toggle whether objects in group are disabled.

  \param waypointGroup a waypoint group object
*/
void WayPointGroupToggle(object waypointGroup);

/**
  \brief Delete an object.

  \param id an object id
*/
void Delete(int id);

/**
  \brief Delete objects in a group.

  \param objectGroup an object group object
*/
void GroupDelete(object objectGroup);

/**
  \brief Cause an object to wander.

  This will cause a NPC or monster to wander.

  \param id an object id
*/
void Wander(int id);

/**
  \brief Cause objects in a group to wander.

  \param objectGroup an object group object
*/
void GroupWander(object objectGroup);

/**
  \private
  \brief Unused.

  This will not do anything.

  \param id an object id
*/
void Unused1f(int id);

/**
  \private
  \brief Unused.

  This will not do anything.

  \param id an object id
*/
void Unused20(int id);

/**
  \brief Cause object to move to its starting location.

  \param id an object id
*/
void GoBackHome(int id);

/**
  \brief Play an audio event at a location.

  \param audio a audio event name ::AudioEvent
  \param waypoint a waypoint object
*/
void AudioEvent(string audio, object waypoint);

/**
  \brief Display a localized string.

  This will display on a localized string on the screen of SELF. If the string
  is not in the string database, it will instead print an error message with
  "MISSING:".

  \param message a string
*/
void Print(string message);

/**
  \brief Display a localized string to everyone.

  This will display on a localized string on everyone's screen. If the string
  is not in the string database, it will instead print an error message with
  "MISSING:".

  \param message a string
*/
void PrintToAll(string message);

/**
  \brief Cause an object to say a localized string.

  This will display a localized string in a speech bubble. If the string
  is not in the string database, it will instead print an error message with
  "MISSING:".

  \param id an object id
  \param message a string
*/
void Chat(int id, string message);

/**
  \brief Exit current script function.

  \param value the function return value, if it is non-void
*/
void StopScript(any value);

/**
  \brief Unlock a door.

  This will unlock a door. It has no effect if the object is not a door.

  \param id an object id
*/
void UnlockDoor(int id);

/**
  \brief Lock a door.

  This will lock a door. It has no effect if the object is not a door.

  \param id an object id
*/
void LockDoor(int id);

/**
  \brief Get whether object is enabled.

  \param id an object id
  \return enabled state as TRUE or FALSE
*/
int IsObjectOn(int id);

/**
  \brief Get whether waypoint is enabled.

  \param waypoint a waypoint object
  \return enabled state as TRUE or FALSE
*/
int IsWaypointOn(object waypoint);

/**
  \brief Get whether object is locked.

  This will return whether an object is locked. It works with any kind of lock.

  \param id an object id
  \return locked state as TRUE or FALSE
*/
int IsLocked(int id);

/**
  \brief Random number (float).

  \param min minimum value
  \param max maximum value
  \return random value between min and max
*/
float RandomFloat(float min, float max);

/**
  \brief Random number (int).

  \param min minimum value
  \param max maximum value
  \return random value between min and max
*/
int Random(int min, int max);

/**
  \brief Create a timer with delay in seconds with an argument.

  This will create a timer that calls the given script function after a
  delay given in seconds. The given argument will be passed into the script
  function.

  \param seconds delay
  \param argument function argument
  \param callback a script function
  \return timer id
*/
int SecondTimerWithArg(int seconds, any argument, function callback);

/**
  \brief Create a timer with delay in frames with an argument.

  This will create a timer that calls the given script function after a
  delay given in frames. The given argument will be passed into the script
  function.

  \param frames delay
  \param argument function argument
  \param callback a script function
  \return timer id
*/
int FrameTimerWithArg(int frames, any argument, function callback);

/**
  \brief Convert an integer to a string.

  This will convert an integer to a string, and add the string to the string
  table temporarily.

  \param number a integer number
  \return a string
*/
string IntToString(int number);

/**
  \brief Convert a float to a string.

  This will convert a float to a string, and add the string to the string
  table temporarily.

  \param number a float number
  \return a string
*/
string FloatToString(float number);

/**
  \brief Create an object at a location.

  This will create an object given a type and a starting location.

  Example usage:
    int spider = CreateObject("SmallAlbinoSpider", Waypoint("SpiderHole"))

  \param type an object type string
  \param waypoint a waypoint object
  \return an object id
*/
int CreateObject(string type, object waypoint);

/**
  \brief Damages an object.

  This will damage the target with a given source object, amount, and damage
  type.

  \param target an object id that receives damage
  \param source an object id as source of damange
  \param amount amount of damage
  \param type type of damange ::DamageType
*/
void Damage(int target, int source, int amount, int type);

/**
  \brief Damages objects in a group.

  This will damage the target objects with a given source object, amount, and
  damage type.

  \param targetGroup an object group object that receives damage
  \param source an object id as source of damange
  \param amount amount of damage
  \param type type of damange ::DamageType
*/
void GroupDamage(object targetGroup, int source, int amount, int type);

/**
  \brief Creates a Mover for an object.

  \param id an object id
  \param arg2 integer
  \param arg3 float
  \return object id of new Mover
*/
int CreateMover(int id, int arg2, float arg3);

/**
  \brief Creates a Mover for every object in a group.

  \param objectGroup an object group object
  \param arg2 integer
  \param arg3 float
*/
void GroupCreateMover(object objectGroup, int arg2, float arg3);

/**
  \brief Award spell level to object.

  This will raise the spell level of the object. If the object can not cast
  this spell then it will have no effect.

  \param id an object id
  \param spell a spell name ::Spell
  \return success as TRUE or FALSE
*/
int AwardSpell(int id, string spell);

/**
  \brief Award spell level to objects in a group.

  This will raise the spell level of the objects in the group. If an object can
  not cast this spell then it will have no effect on that object.

  \param objectGroup an object group object
  \param spell a spell name ::Spell
*/
void GroupAwardSpell(object objectGroup, string spell);

/**
  \brief Grant object an enchantment.

  This will grant an object an enchantment of a specified duration. If the
  enchantment name is incorrect, the game may crash.

  \param id an object id
  \param enchant an enchantment name ::Enchant
  \param duration in seconds
*/
void Enchant(int id, string enchant, float duration);

/**
  \brief Grant objects in a group an enchantment.

  This will grant the objects in a group an enchantment of a specified
  duration. If the enchantment name is incorrect, the game may crash.

  \param id an object id
  \param enchant an enchantment name ::Enchant
  \param duration in seconds
*/
void GroupEnchant(int id, string enchant, float duration);

/**
  \brief Get host's player object.

  This will return the host's player object id. The host is the player with
  a player id of 31.

  \return an object id
*/
int GetHost();

/**
  \brief Lookup an object by name.

  This will lookup an object by its script name and return the object id.

  \param name object name
  \return an object id
*/
int Object(string name);

/**
  \brief Get object X coordinate.

  \param id an object id
  \return x coordinate
*/
float GetObjectX(int id);

/**
  \brief Get waypoint X coordinate.

  \param waypoint a waypoint object
  \return x coordinate
*/
float GetWaypointX(object waypoint);

/**
  \brief Get object Y coordinate.

  \param id an object id
  \return y coordinate
*/
float GetObjectY(int id);

/**
  \brief Get waypoint Y coordinate.

  \param waypoint a waypoint object
  \return y coordinate
*/
float GetWaypointY(object waypoint);

/**
  \brief Get object Z coordinate.

  \param id a object id
  \return z coordinate
*/
float GetObjectZ(int id);

/**
  \brief Get object direction.

  See the description of ::LookWithAngle.

  \param id a object id
  \return
*/
int GetDirection(int id);

/**
  \brief Set an object's location.

  \param id an object id
  \param x x coordinate 
  \param y y coordinate 
*/
void MoveObject(int id, float x, float y);

/**
  \brief Set a waypoint's location.

  \param waypoint a waypoint object
  \param x x coordinate 
  \param y y coordinate 
*/
void MoveWaypoint(object waypoint, float x, float y);

/**
  \brief Set an object's Z coordinate.

  This will set an object's Z coordinate and then let the object fall down.

  \param id an object id
  \param z z coordinate
*/
void Raise(int id, float z);

/**
  \brief Set an object's direction.

  This will set an object's direction. The direction is an angle
  represented as an integer between 0 and 255. Due east is 0, and the angle
  increases as the object turns clock-wise.

  \param id an object id
  \param angle a number between 0 and 255
*/
void LookWithAngle(int id, int angle);
/**
  \brief Push an object to a location.

  \param id an object id
  \param x x coordinate
  \param y y coordinate
*/
void PushObjectTo(int id, float x, float y);

/**
  \brief Push an object from a vector and magnitude.

  This will calculate a unit vector from the object's location to the specified
  location, and multiply it by the specified magnitude. This vector will be
  added to the object's location.

  \param id an object id
  \param magnitude force magnitude
  \param x force x coordinate
  \param y force y coordinate
*/
void PushObject(int id, float magnitude, float x, float y);

/**
  \brief Get object's last inventory item.

  This will return the object id of the last item in the object's inventory.
  If the inventory is empty, it will return 0.

  This is used with ::GetPreviousItem to iterate through an object's inventory.

  \param id an object id
  \return an object id, or 0
*/
int GetLastItem(int id);

/**
  \brief Get previous inventory item.

  This will return the object id of the previous item in the inventory from
  the given object id. If the specified object id is not in an inventory, or
  there are no more items in the inventory, it will return 0;

  This is used with ::GetLastItem to iterate through an object's inventory.

  \param id an object id
  \return an object id, or 0
*/
int GetPreviousItem(int id);

/**
  \brief Get whether the item is in the object's inventory.

  \param holder an object id with inventory to check
  \param item an object id of item to check for
  \return TRUE or FALSE
*/
int HasItem(int holder, int item);

/**
  \brief Get the holder of an item.

  This will return the object id that contains the item in its inventory.

  \param item an object id
  \return an object id of the holder
*/
int GetHolder(int item);

/**
  \brief Cause object to pickup an item.

  \param id an object id
  \param item an object id to pickup
  \return success as TRUE or FALSE
*/
int Pickup(int id, int item);

/**
  \brief Cause object to drop an item.

  \param id an object id
  \param item an object id to drop
  \return success as TRUE or FALSE
*/
int Drop(int id, int item);

/**
  \brief Get whether object has a class.

  \param id an object id
  \param className a class name ::Class
  \return TRUE or FALSE
*/
int HasClass(int id, string className);

/**
  \private
  \brief Unused.

  Does nothing.
*/
void Unused50();

/**
  \brief Get whether object has an enchant.

  \param id an object id
  \param enchant an enchant name ::Enchant
  \return TRUE or FALSE
*/
int HasEnchant(int id, string enchant);

/**
  \brief Remove enchant from an object.

  \param id an object id
  \param enchant an enchant name ::Enchant
*/
void EnchantOff(int id, string enchant);

/**
  \brief Get object's health.

  \param id an object id
  \return health
*/
int CurrentHealth(int id);

/**
  \brief Get object's maximum health.

  \param id an object id
  \return max mealth
*/
int MaxHealth(int id);

/**
  \brief Restore object's health.

  \param id an object id
  \param amount amount of health to restore
*/
void RestoreHealth(int id, int amount);

/**
  \brief Calculate distance between two locations.

  \param x1
  \param y1
  \param x2
  \param y2
  \return distance
*/
float Distance(float x1, float y1, float x2, float y2);

/**
  \brief Gets whether an object can see another object.

  This will first check if the location of the objects are within 512 of each
  other coordinate-wise. It not, it returns FALSE.

  It then checks whether the first object can see the second object.

  \param object1 an object id
  \param object2 an object id
  \return TRUE or FALSE
*/
int IsVisibleTo(int object1, int object2);

/**
  \private
  \brief Unused.

  Does nothing.
*/
void Unused58(int arg1, int arg2);

/**
  \private
  \brief Unused.

  Does nothing.
*/
void Unused59(int arg1, int arg2);

/**
  \private
  \brief Unused.

  Does nothing.
*/
void Unused5a(int arg1, int arg2);

/**
  \private
  \brief Unused.

  Does nothing.
*/
void Unused5b(int arg1, int arg2);

/**
  \private
  \brief Unused.

  Does nothing.
*/
void Unused5c(int arg1, int arg2);

/**
  \private
  \brief Unused.

  Does nothing.
*/
void Unused5d(int arg1, int arg2);

/**
  \private
  \brief Unused.

  Localizes a string. Output is useless however.

  \param str a string
  \return an index
*/
int Unused5e(string str);

/**
  \brief Get character data.

  FIXME

  Get information about the loaded character.

  \param idx what to return (0-5)
  \return value
*/
int GetCharacterData(int idx);

/**
  \brief Set direction of object so it is looking at another object.

  \param id an object id
  \param target an object id to look at
*/
void LookAtObject(int id, int target);

/**
  \brief Causes an object to walk to a location.

  \param id an object id
  \param x x coordinate
  \param y y coordinate
*/
void Walk(int id, float x, float y);

/**
  \brief Causes objects in a group to walk to a location.

  \param objectGroup an object group object
  \param x x coordinate
  \param y y coordinate
*/
void GroupWalk(object objectGroup, float x, float y);

/**
  \brief Cancel a timer

  \param id a timer id
  \return success as TRUE or FALSE
*/
int CancelTimer(int id);

/**
  \brief Trigger an effect

  This will trigger an effect from point (x1,y1) to (x2,y2). Some effects only
  have one point, in which case (x2,y2) is ignored.

  \param effect an effect name ::Effect
  \param x1
  \param y1
  \param x2
  \param y2
*/
void Effect(string effect, float x1, float y1, float x2, float y2);

/**
  \brief Set the owner of an object.

  This will make an object the owner of the target. This will make the target
  friendly to the owner, and it will accredit the target's kills to the owner.

  For example, in a multiplayer map, you might have a switch that activates a
  hazard. You can use this so that if the hazard kills anyone, the player who
  activated the hazard gets the credit.

  \param owner an object id
  \param target an object id
*/
void SetOwner(int owner, int target);

/**
  \brief Set the owner of objects in a group.

  This is the same as ::SetOwner but with a object group as the target.

  \param owner an object id
  \param targets an object group object
*/
void GroupSetOwner(int owner, object targets);

/**
  \brief Set the objects in a group as owners of target.

  This is the same as ::SetOwner but with a object group as the owner.

  \param owners an object group object
  \param target an object id
*/
void SetOwners(object owners, int target);

/**
  \brief Set the objects in a group as owners of target.

  This is the same as ::SetOwners but with a object group as the target.

  \param owners an object group object
  \param targets an object group object
*/
void GroupSetOwners(object owners, object targets);

/**
  \brief Get whether target is owned by object.

  \param id an object id
  \param target an object id
  \return TRUE or FALSE
*/
int IsOwnedBy(int id, int target);

/**
  \brief Get whether any object in target group is owned by object.

  \param id an object id
  \param target an object group object
  \return TRUE or FALSE
*/
int GroupIsOwnedBy(int id, object target);

/**
  \brief Get whether target is owned by any object in the group.

  \param objectGroup an object group object
  \param target an object id
  \return TRUE or FALSE
*/
int IsOwnedByAny(object objectGroup, int target);

/**
  \brief Get whether any object in target is owned by any object in the group.

  \param objectGroup an object group object
  \param target an object group object
  \return TRUE or FALSE
*/
int GroupIsOwnedByAny(object objectGroup, object target);

/**
  \brief Clear the owner of an object

  \param id an object id
*/
void ClearOwner(int id);

/**
  \brief Lookup waypoint by name.

  \param name a waypoint name
  \return a waypoint object
*/
object Waypoint(string name);

/**
  \brief Lookup waypoint group by name.

  \param name a waypoint group name
  \return a waypoint group object
*/
object WaypointGroup(string name);

/**
  \brief Lookup object group by name.

  \param name a object group name
  \return a object group object
*/
object ObjectGroup(string name);

/**
  \brief Lookup wall group by name.

  \param name a wall group name
  \return a wall group object
*/
object WallGroup(string name);

/**
  \brief Cause an object to say a localized string for duration in seconds.

  This will display a localized string in a speech bubble. If the string
  is not in the string database, it will instead print an error message with
  "MISSING:".

  \param id an object id
  \param message a string
  \param duration in seconds
*/
void ChatTimerSeconds(int id, string message, int duration);

/**
  \brief Cause an object to say a localized string for duration in frames.

  This will display a localized string in a speech bubble. If the string
  is not in the string database, it will instead print an error message with
  "MISSING:".

  \param id an object id
  \param message a string
  \param duration in frames
*/
void ChatTimer(int id, string message, int duration);

/**
  \private
  \brief Unused.

  Does nothing.
*/
void Unused74(int arg1, int arg2);

/**
  \brief Destroys object's speech bubble.

  \param id an object id
*/
void DestroyChat(int id);

/**
  \brief Destroys all speech bubbles.
*/
void DestroyEveryChat();

/**
  \brief Set quest status (int).

  \param status value to save
  \param name quest name
*/
void SetQuestStatus(int status, string name);

/**
  \brief Set quest status (float).

  \param status value to save
  \param name quest name
*/
void SetQuestStatusFloat(float status, string name);

/**
  \brief Get quest status (int).

  \param name quest name
*/
void GetQuestStatus(string name);

/**
  \brief Get quest status (int).

  \param name quest name
*/
void GetQuestStatusFloat(string name);

/**
  \brief Delete quest status.

  This will delete a quest status. The name can be a wildcard with an
  asterisk or with a map name.
  
  TODO what is the wildcard syntax?

  \param name quest name
*/
void ResetQuestStatus(string name);

/**
  \brief Get whether object is OTHER.

  \param id an object id
*/
void IsTrigger(int id);

/**
  \brief Get whether object is SELF.

  \param id an object id
*/
void IsCaller(int id);

/**
  \brief Setup a conversation with object.

  This will cause a conversation with the object. The type of conversation is
  one of: NORMAL, NEXT, YESNO, YESNONEXT. The start and end are script
  functions that are called at the start and end of the conversation.

  If using a YESNO conversation, the end script function should use ::GetAnswer
  to retrieve the result.

  \param id an object id
  \param type a conversation type string (NORMAL, NEXT, YESNO, YESNONEXT)
  \param start a script function
  \param end a script function
*/
void SetDialog(int id, string type, function start, function end);

/**
  \brief Cancel a conversation with object.

  \param id an object id
*/
void CancelDialog(int id);

/**
  \brief Assigns a picture to a conversation.

  \param id an object id
  \param name a picture name
*/
void StoryPic(int id, string name);

/**
  \brief Causes the telling of a story.

  This will cause a story to be told. It relies on SELF and OTHER to be
  particular values, which limits this to being used in the ::SetDialog
  callbacks.

  Example usage:
    TellStory("SwordsmanHurt", "Con05:OgreTalk07")

  \param audio an audio event name that is usually "SwordsmanHurt"
  \param story a story name
*/
void TellStory(string audio, string story);

/**
  \brief Starts a conversation between two objects.

  This requires that SetDialog has already been used to setup the conversation
  on the NPC object.

  \param npc an object id
  \param other an object id
*/
void StartDialog(int npc, int other);

/**
  \brief Casts a spell from source to target.

  Example usage:
    CastSpellOn("SPELL_DEATH_RAY", Object("CruelDude"), GetHost())

  \param spell a spell name ::Spell
  \param source an object id
  \param target an object id
*/
void CastSpellObjectObject(string spell, int source, int target);

/**
  \brief Casts a spell from source to target.

  \param spell a spell name ::Spell
  \param source an object id
  \param x target x coordinate
  \param y target y coordinate
*/
void CastSpellObjectLocation(string spell, int source, float x, float y);

/**
  \brief Casts a spell from source to target.

  \param spell a spell name ::Spell
  \param x source x coordinate
  \param y source y coordinate
  \param target an object id
*/
void CastSpellLocationObject(string spell, float x, float y, int target);

/**
  \brief Casts a spell from source to target.

  \param spell a spell name ::Spell
  \param x1 source x coordinate
  \param y1 source y coordinate
  \param x2 target x coordinate
  \param y2 target y coordinate
*/
void CastSpellLocationLocation(string spell, float x1, float y1, float x2, float y2);

/**
  \brief Unblind the host.
*/
void UnBlind();

/**
  \brief Blind the host.
*/
void Blind();

/**
  \param value TRUE or FALSE
*/
void WideScreen(int value);

/**
  \brief Get elevator status.

  \param id an object id
  \return status, or -1 if invalid object
*/
int GetElevatorStatus(int id);

/**
  \brief Cause a creature to guard a location.

  This will cause a creature to move to a location, guard a nearby location,
  and attack any enemies that move within range of the guarded location.

  \param id an object id
  \param x1 x coordinate to guard from
  \param y1 y coordinate to guard from
  \param x2 x coordinate to watch
  \param y2 y coordinate to watch
  \param distance distance from (x2,y2) to attack
*/
void CreatureGuard(int id, float x1, float y1, float x2, float y2, float distance);

/**
  \brief Cause creatures in a group to guard a location.

  This is the same as ::CreatureGuard but applies to creatures in a group.

  \param objectGroup an object group object
  \param x1 x coordinate to guard from
  \param y1 y coordinate to guard from
  \param x2 x coordinate to watch
  \param y2 y coordinate to watch
  \param distance distance from (x2,y2) to attack
*/
void CreatureGroupGuard(object objectGroup, float x1, float y1, float x2, float y2, float distance);

/**
  \brief Cause creature to hunt.

  \param id an object id
*/
void CreatureHunt(int id);

/**
  \brief Cause creatures in a group to hunt.

  \param objectGroup an object group object
*/
void CreatureGroupHunt(object objectGroup);

/**
  \brief Cause creature to idle.

  \param id an object id
*/
void CreatureIdle(int id);

/**
  \brief Cause creatures in a group to idle.

  \param objectGroup an object group object
*/
void CreatureGroupIdle(object objectGroup);

/**
  \brief Cause creature to follow an object.

  This will cause a creature to follow target, and it won't attack anything
  unless disrupted or instructed to.

  \param id an object id
  \param target an object id
*/
void CreatureFollow(int id, int target);

/**
  \brief Cause creatures in a group to follow an object.

  This will cause the creatures to follow target, and they won't attack
  anything unless disrupted or instructed to.

  \param objectGroup an object group object
  \param target an object id
*/
void CreatureGroupFollow(object objectGroup, int target);

/**
  \brief Set creature's aggression level.

  This will set a creature's aggression level. The most commonly used value
  is 0.83.

  \param id an object id
  \param level aggression level
*/
void AggressionLevel(int id, float level);

/**
  \brief Set group of creature's aggression level.

  This will set a group of creature's aggression level. The most commonly used
  value is 0.83.

  \param objectGroup an object group object
  \param level aggression level
*/
void GroupAggressionLevel(object objectGroup, float level);

/**
  \brief Melee attack a location.

  \param id an object id
  \param x x coordinate
  \param y y coordinate
*/
void HitLocation(int id, float x, float y);

/**
  \brief Melee attack a location.

  \param objectGroup an object group object
  \param x x coordinate
  \param y y coordinate
*/
void GroupHitLocation(object objectGroup, float x, float y);

/**
  \brief Ranged attack a location.

  \param id an object id
  \param x x coordinate
  \param y y coordinate
*/
void HitFarLocation(int id, float x, float y);

/**
  \brief Ranged attack a location.

  \param objectGroup an object group object
  \param x x coordinate
  \param y y coordinate
*/
void GroupHitFarLocation(object objectGroup, float x, float y);

/**
  \brief Set roaming flags.

  \param id an object id
  \param flags a 8-bit value (default is 0x80)
*/
void SetRoamFlag(int id, int flags);

/**
  \brief Set roaming flags.

  \param objectGroup an object group object
  \param flags a 8-bit value (default is 0x80)
*/
void GroupSetRoamFlag(object objectGroup, int flags);

/**
  \brief Attack an object.

  \param id an object id
  \param target an object id
*/
void Attack(int id, int target);

/**
  \brief Attack an object.

  \param objectGroup an object group object
  \param target an object id
*/
void GroupAttack(object objectGroup, int target);

/**
  \brief Add entry to player's journal.

  This will add an entry to a player object's journal. The string can be any
  string, but should be less than 64 characters. The string is displayed
  according to the specified type:

    0 = Green text, no sound
    1 = White text
    2 = Red text with quest label
    3 = Green text
    4 = Grey text with completed label
    8 = Yellow text with hint label

  If the player object id is 0, then it will add the journal entry to all
  players.

  \param id an object id of player, or 0 for all players
  \param message string less than 64 characters
  \param type see description
*/
void JournalEntry(int id, string message, int type);

/**
  \brief Delete entry from player's journal.

  This will delete the first entry from a player object's journal whose message
  matches the specified message. If the player object id is 0, then all players
  are affected.

  \param id an object id of player, or 0 for all players
  \param message entry to delete
*/
void JournalDelete(int id, string message);

/**
  \brief Edit entry in player's journal.

  This will modify the first entry in a player object's journal whose message
  matches the specified message. If the player object id is 0, then all players
  are affected.

  \param id an object id of player, or 0 for all players
  \param message entry to edit
  \param type see description of ::JournalEntry
*/
void JournalEdit(int id, string message, int type);

/**
  \brief Set when creature retreats due to low health.

  This will cause the creature to retreat if its health falls below the
  specified percentage.

  \param id an object id
  \param percent low health ratio (0.0 - 1.0)
*/
void RetreatLevel(int id, float percent);

/**
  \brief Set when creature retreats due to low health.

  This will cause the creatures to retreat if its health falls below the
  specified percentage.

  \param objectGroup an object group object
  \param percent low health ratio (0.0 - 1.0)
*/
void GroupRetreatLevel(object objectGroup, float percent);

/**
  \brief Set when creature resumes due to health.

  This will cause the creature to stop retreating if its health is above the
  specified percentage.

  \param id an object id
  \param percent health ratio (0.0 - 1.0)
*/
void ResumeLevel(int id, float percent);

/**
  \brief Set when creature resumes due to health.

  This will cause the creatures to stop retreating if its health is above the
  specified percentage.

  \param objectGroup an object group object
  \param percent health ratio (0.0 - 1.0)
*/
void GroupResumeLevel(object objectGroup, float percent);

/**
  \brief Cause creature to run away from target.

  \param id creature's object id
  \param target an object id to run away from
  \param duration number of frames
*/
void RunAway(int id, int target, int duration);

/**
  \brief Cause creatures to run away from target.

  \param objectGroup an object group object
  \param target an object id to run away from
  \param duration number of frames
*/
void GroupRunAway(object objectGroup, int target, int duration);

/**
  \brief Pause an object temporarily.

  \param id an object id
  \param duration number of frames
*/
void PauseObject(int id, int duration);

/**
  \brief Pause objects of a group temporarily.

  \param objectGroup an object group object
  \param duration number of frames
*/
void GroupPauseObject(object objectGroup, int duration);

/**
  \brief Get whether object1 is being attacked by object2.

  \param id1 an object id
  \param id2 an object id
*/
int IsAttackedBy(int id1, int id2);

/**
  \brief Get amount of gold for player object.

  \param id an object id
  \return amount of gold
*/
int GetGold(int id);

/**
  \brief Change amount of gold for player object.

  \param id an object id
  \param delta amount to add (can be negative)
*/
void ChangeGold(int id, int delta);

/**
  \brief Get answer from conversation.

  \param id an object id
  \return result (0=Goodbye, 1=Yes, 2=No)
*/
int GetAnswer(int id);

/**
  \brief Grant experience to a player.

  \param id an object id
  \param xp experience to gain
*/
void GiveXp(int id, float xp);

/**
  \brief Get whether item has subclass.

  This will test whether an item has a specifiec subclass. The subclass
  overlaps, so only test for subclasses that are valid for this item.

  \param id an object id
  \param subclass a subclass name
  \return TRUE or FALSE
*/
void ItemHasSubclass(int id, string subclass);

/**
  \brief Trigger an autosave. Only solo games.
*/
void AutoSave();

/**
  \brief Plays music.

  \param music music id
  \param volume number from 0 - 100
*/
void Music(int music, int volume);

/**
  \brief Show startup screen to host.

  \param arg1
*/
void StartupScreen(int arg1);

/**
  \brief Get whether host is talking.

  \return TRUE or FALSE
*/
int IsTalking();

/**
  \brief Get OTHER if valid.

  \return an object id, or 0
*/
int GetTrigger();

/**
  \brief Get SELF if valid.

  \return an object id, or 0
*/
int GetCaller();

/**
  \brief Set object friendly with host.

  \param id an object id
*/
void MakeFriendly(int id);

/**
  \brief Unset object as friendly.

  \param id an object id
*/
void MakeEnemy(int id);

/**
  \brief Set object as pet of host.

  \param id an object id
*/
void BecomePet(int id);

/**
  \brief Unset object as pet of host.

  \param id an object id
*/
void BecomeEnemy(int id);

/**
  TODO

  \param id an object id
  \return TRUE or FALSE
*/
int Unknownb8(int id);

/**
  TODO

  \param id an object id
  \return TRUE or FALSE
*/
int Unknownb9(int id);

/**
  \brief Upgrade host's oblivion staff.

  This will upgrade the oblivion staff. The upgrades are:

    0 = OblivionHalberd
    1 = OblivionHeart
    2 = OblivionWierdling
    3 = OblivionOrb

  \param upgrade see description
*/
void SetHalberd(int upgrade);

/**
  \brief Show death screen.

  \param type one of 0=Warrior, 1=Wizard, 2=Conjurer
*/
void DeathScreen(int type);

/**
  \brief Set frozen status of an object.

  \param id an object id
  \param frozen either TRUE (1) or FALSE (0)
*/
void Frozen(int id, int frozen);

/**
  \brief Set no wall sound flag.

  \param noWallSound either TRUE (1) or FALSE (0)
*/
void NoWallSound(int noWallSound);

/**
  \brief Set a callback on an object.

  This will set a function script to call for an event. The callback index is
  one of the following:

    3 = Enemy sighted
    4 = Looking for enemy
    5 = Deatch
    6 = Change focus
    7 = Is hit
    8 = Retreat
    9 = Collision
    10 = Enemy heard
    11 = End of waypoint
    13 = Lost sight of enemy

  No other indexes are defined.

  \param id an object id
  \param idx callback index
  \param callback a script function
*/
void SetCallback(int id, int idx, function callback);

/**
  \brief Delete object after a delay.

  \param id an object id
  \param delay number of frames
*/
void DeleteObjectTimer(int id, int delay);

/**
  \brief Set spells on a bomber.

  \param id an object id
  \param spell1 a spell name, or NULL ::Spell
  \param spell2 a spell name, or NULL ::Spell
  \param spell3 a spell name, or NULL ::Spell
*/
void TrapSpells(int id, string spell1, string spell2, string spell3);

/**
  \brief Get whether the host is currently trading.

  This will return whether the host is currently talking to shopkeeper.

  \return TRUE or FALSE
*/
int IsTrading();

/**
  \brief Clear messages on player's screen.

  \param id an object id
*/
void ClearMessages(int id);

/**
  \brief Set shopkeeper text.

  \param id an object id
  \param text a string less than 32 characters
*/
void SetShopkeeperText(int id, string text);

/**
  TODO
*/
void Unknownc4();

/**
  \brief Gets whether object is a summoned creature.

  \param id an object id
  \return TRUE or FALSE
*/
int IsSummoned(int id);

/**
  \brief Set zombie to stay down.

  \param id an object id
*/
void ZombieStayDown(int id);

/**
  \brief Set group of zombies to stay down.

  \param objectGroup an object group object
*/
void ZombieGroupStayDown(object objectGroup);

/**
  \brief Raise a zombie. Also clears stay down state.

  \param id an object id
*/
void RaiseZombie(object int id);

/**
  \brief Raise a zombie. Also clears stay down state.

  \param objectGroup an object group object
*/
void RaiseZombieGroup(object objectGroup);

/**
  TODO
*/
void MusicPushEvent();

/**
  TODO
*/
void MusicPopEvent();

/**
  TODO
*/
void MusicEvent();

/**
  \brief Get whether object is a GameBall.

  \param id an object id
  \return TRUE or FALSE
*/
int IsGameBall(int id);

/**
  \brief Get whether object is a Crown.

  \param id an object id
  \return TRUE or FALSE
*/
int IsCrown(int id);

/**
  \brief End of game.

  \param type one of 0=Warrior, 1=Wizard, 2=Conjurer
*/
void EndGame(int type);

/**
  \brief Immediately blind the host.

  \sa ::Blind
*/
void ImmediateBlind();

/**
  \brief Set player object's team

  \param id an object id
  \param team team number
*/
void SetTeam(int id, int team);

/**
  \brief Get player object's team

  \param id an object id
  \return team number
*/
int GetTeam(int id);

/**
 * Singleton site data: identity, career, education, funding, links.
 *
 * Lists that grow (publications, talks, service, posts) are content
 * collections instead — see src/content.config.ts. This file is for the things
 * there is exactly one of.
 */

export const profile = {
  name: 'Dr. Emanuel Lacić',
  shortName: 'Emanuel Lacić',
  /** Used to emphasise your own name in author lists. */
  surnameForms: ['Lacić', 'Lacic'],
  role: 'Principal Engineer',
  team: 'Team AI Research (AIR)',
  employer: 'Infobip',
  location: 'Zagreb, Croatia',
  email: 'emanuel.lacic@infobip.com',
  /** Obfuscated form for display, to keep naive scrapers off it. */
  emailDisplay: 'emanuel [dot] lacic [at] infobip [dot] com',

  /** The hero. Three lines that set, then a quieter fourth. */
  statement: {
    lines: ['AI Research at Infobip,', 'building AI for global communication'],
    coda: '— and discover what comes up next.',
  },

  /** Portrait used in the hero margin (same asset as v1’s sidebar). */
  photo: '/images/profile2.jpg',

  /** The working note in the hero margin. */
  workingNote:
    'A working record of research I’m doing now. Findings, open questions, and the direction I expect to push for years ahead.',

  /** Research keywords, set like the keyword line of a paper. Six at most. */
  keywords: [
    'Recommender systems',
    'Generative AI & LLMs',
    'Fairness & bias',
    'Real-time personalization',
    'Information retrieval',
    'Evaluation & reproducibility',
  ],

  /** Longer bio for /cv and meta descriptions. */
  bio: `Emanuel Lacić leads Team AI Research at Infobip, an R&D team working on applied AI for communication at global scale, with a current focus on generative AI and the practical impact of large language models. He previously led the Fair-AI division at the Know-Center, Austria's research centre for data-driven business, and holds a PhD with distinction from Graz University of Technology. He is a former Marshall Plan fellow and visiting researcher at UCLA, and special issue editor of Frontiers in Big Data — Recommender Systems. His research concerns recommender systems and information retrieval, with a focus on algorithmic accuracy, real-time performance, privacy, fairness and bias.`,

  links: {
    scholar: 'https://scholar.google.com/citations?hl=en&user=-Bb4HhQAAAAJ&view_op=list_works&sortby=pubdate',
    linkedin: 'https://linkedin.com/in/elacic',
    researchgate: 'https://www.researchgate.net/profile/Emanuel_Lacic',
    twitter: 'https://twitter.com/elacic1',
    infobipResearch: 'https://research.infobip.com/',
    cv: '/documents/elacic_cv.pdf',
  },
} as const;

/** Team AIR members shown on /air. Order is intentional. */
export type AirMember = {
  name: string;
  role: string;
  photo: string;
  url?: string;
  /** Personal blog index, when they write publicly. */
  blog?: string;
  /** RSS feed used for the team-section blog invite under the roster. */
  feed?: string;
  /**
   * Fallback for the team blog invite when the live feed cannot be fetched
   * (offline `astro dev`, flaky network). Prefer the feed when it resolves;
   * bump this when you notice a new post and the build machine is offline.
   */
  latestPost?: { title: string; link: string; date: string };
  scholar?: string;
};

export const airTeam: AirMember[] = [
  {
    name: 'Ante Kapetanović',
    role: 'Senior AI Research Scientist',
    photo: '/images/team/ante-kapetanovic.jpg',
    url: 'https://antekapetanovic.com/',
    blog: 'https://antekapetanovic.com/blog/',
    feed: 'https://antekapetanovic.com/index.xml',
    latestPost: {
      title: 'How Far Can an Agentic Research Loop Push a Standard Computer Graphics Baseline?',
      link: 'https://antekapetanovic.com/blog/phased-agent-normal-estimation/',
      date: '2026-07-26',
    },
    scholar: 'https://scholar.google.com/citations?user=oAShnpsAAAAJ&hl=en',
  },
  {
    name: 'Tomislav Đuričić',
    role: 'Senior AI Research Scientist',
    photo: '/images/team/tomislav-duricic.jpg',
    url: 'https://tduricic.me/',
    scholar: 'https://scholar.google.com/citations?user=_mY5j2UAAAAJ&hl=en',
  },
  {
    name: 'Andro Merćep',
    role: 'Senior AI Research Scientist',
    photo: '/images/team/andro-mercep.jpg',
    scholar: 'https://scholar.google.com/citations?user=qtDNIKsAAAAJ&hl=hr',
  },
  {
    name: 'Dionizije Fa',
    role: 'Senior AI Research Scientist',
    photo: '/images/team/dionizije-fa.jpg',
    url: 'https://dionizijefa.com/',
    scholar: 'https://scholar.google.com/citations?user=bjqVJYkAAAAJ&hl=en',
  },
];

export type CareerRole = {
  years: string;
  title: string;
  detail?: string;
  /** A concurrent engagement rather than a subsequent role. */
  concurrent?: boolean;
  tag?: string;
};

export type CareerEntry = {
  org: string;
  place: string;
  span: string;
  url?: string;
  /** Set for pre-2013 roles, which render quietly so recent work still leads. */
  early?: boolean;
  /**
   * Include in the landing-page “career in brief”. Defaults to `!early`.
   * Set false for mid-career roles that still belong on /cv but not the home list.
   */
  inBrief?: boolean;
  current?: boolean;
  roles: CareerRole[];
};

/**
 * Grouped by organisation, because a reader orients by place: "seven years at
 * Know-Center" is the fact they retain, and the internal promotion is detail
 * underneath it. A flat chronological list would make one continuous tenure
 * look like two short ones.
 *
 * The two Infobip entries stay separate and unannotated. Merging them would
 * imply continuous employment that did not happen; the dates say the rest.
 */
export const career: CareerEntry[] = [
  {
    org: 'Infobip',
    place: 'Zagreb',
    span: '2023 —',
    url: 'https://www.infobip.com/',
    current: true,
    roles: [
      {
        years: '2023 —',
        title: 'Principal Engineer',
        detail: 'Team AI Research. Focus on generative AI and the impact of LLMs.',
      },
    ],
  },
  {
    org: 'Know-Center',
    place: 'Graz',
    span: '2016—2023',
    url: 'https://www.know-center.at/',
    roles: [
      {
        years: '2021—23',
        title: 'Operations Area Manager, Fair-AI',
        detail: 'Led the research division on applied recommender systems, fairness and social network analysis.',
      },
      {
        years: '2016—20',
        title: 'Senior Researcher & Recommender Systems Architect',
        detail: 'Management, lead development and consulting on industry recommender system projects.',
      },
    ],
  },
  {
    org: 'Graz University of Technology',
    place: 'Graz',
    span: '2013—2016',
    url: 'https://www.tugraz.at/en/home/',
    inBrief: false,
    roles: [
      {
        years: '2013—16',
        title: 'University & Project Assistant',
        detail: 'Knowledge extraction and social network data on the EU FP7 project Learning Layers.',
      },
    ],
  },
  {
    org: '1&1 Internet AG',
    place: 'Karlsruhe',
    span: '2013',
    url: 'https://www.1und1.de/',
    early: true,
    roles: [{ years: '2013', title: 'Junior Software Developer', detail: 'Ruby, data-centre management and monitoring tooling.' }],
  },
  {
    org: 'FZI Forschungszentrum Informatik',
    place: 'Karlsruhe',
    span: '2012',
    url: 'https://www.fzi.de/en/home/',
    early: true,
    roles: [{ years: '2012', title: 'Java Developer', detail: 'EU FP7 project Mirror.' }],
  },
  {
    org: 'Infobip',
    place: 'Zagreb',
    span: '2011—2012',
    url: 'https://www.infobip.com/',
    early: true,
    roles: [{ years: '2011—12', title: 'Software Engineer', detail: 'Mobile cloud services — SMS, HLR, USSD.' }],
  },
  {
    org: 'Ericsson',
    place: 'Zagreb',
    span: '2010',
    early: true,
    roles: [{ years: '2010', title: 'Java Developer', detail: 'Information system for primary healthcare.' }],
  },
];

/**
 * A separate block, deliberately not merged into the career timeline: the PhD
 * completed in 2022 while the Know-Center role was running, so a single merged
 * list would place a degree between two jobs and imply a career break.
 *
 * `aside` holds a stay that belongs to the degree rather than to a job — the
 * UCLA visit was doctoral research abroad, not a change of employer.
 */
export const education = [
  {
    degree: 'PhD, Computer Science',
    distinction: 'with distinction',
    institution: 'Graz University of Technology',
    place: 'Graz',
    year: 2022,
    aside: {
      year: '2018',
      title: 'Visiting researcher, UCLA Computer Science',
      detail: 'Marshall Plan Fellowship — session-based recommendation.',
      tag: 'visiting',
    },
    links: [
      { label: 'thesis', href: '/documents/2022_phd_cummulative_elacic.pdf' },
      { label: 'defence slides', href: '/documents/phd_rigorosum_short_slides.pdf' },
    ],
  },
  {
    degree: 'M.Sc., Software Engineering & Information Systems',
    institution: 'University of Zagreb, FER',
    place: 'final year at Karlsruhe Institute of Technology',
    year: 2012,
    links: [],
  },
  {
    degree: 'B.Sc., Software Engineering & Information Systems',
    institution: 'University of Zagreb, FER',
    place: 'Zagreb',
    year: 2010,
    links: [],
  },
] as const;

/**
 * Funding, kept separate from awards. An award says other people rated your
 * work; funding says you can be trusted with a budget and a consortium. For
 * someone leading an industrial research team the second is the rarer signal.
 *
 * `amount` is only set where the figure is public. Optional `url` links the
 * project name to a public page.
 */
export const funding = [
  {
    name: 'IPCEI-CIS',
    amount: '€35M',
    kind: 'project grant',
    years: '2024',
    detail: 'Next-Generation Communication Platform · author of the AI Research Strategy for the EU programme',
  },
  {
    name: 'DDIA',
    amount: '€3.7M',
    kind: 'COMET module',
    years: '2022–26',
    detail: 'Data Driven Immersive Analytics in Digital Industries · €350k for FAIR-AI, Know-Center · key researcher for “Personalized Immersive Learning Support”',
    url: 'https://www.know-center.at/en/research/comet-modul/ddia/',
  },
  {
    name: 'Radreisen4All',
    amount: '€150,000',
    kind: 'project grant',
    years: '2022–25',
    detail: 'FFG Femtech · for Fair-AI, Know-Center · key researcher',
    url: 'https://projekte.ffg.at/projekt/4387847',
  },
  {
    name: 'DDAI',
    amount: '€3.7M',
    kind: 'COMET module',
    years: '2020–23',
    detail: 'Explainable, Verifiable and Privacy-Preserving Data-Driven AI · €700k for Social Computing, Know-Center · key researcher for “Explainable AI for Users”',
    url: 'https://www.know-center.at/en/research/comet-modul/ddai-data-driven-artificial-intelligence/',
  },
  {
    name: 'JOLIOO',
    amount: '€120,000',
    kind: 'project grant',
    years: '2020',
    detail: 'FFG Basisantrag · for Social Computing, Know-Center · researcher',
    url: 'https://projekte.ffg.at/projekt/3411124',
  },
  {
    name: 'COGSTEPS',
    amount: '€130,000',
    kind: 'project grant',
    years: '2020–23',
    detail: 'Erasmus+ · for Know-Center and ISDS@TU Graz · researcher',
    url: 'https://cogsteps.com/about/',
  },
  {
    name: 'TRUSTS',
    amount: '€730,000',
    kind: 'project grant',
    years: '2020–22',
    detail: 'H2020 · for Know-Center (€138k for Social Computing) · task leader',
    url: 'https://cordis.europa.eu/project/id/871481',
  },
  {
    name: 'TRIPLE',
    amount: '€377,000',
    kind: 'project grant',
    years: '2019–22',
    detail: 'H2020 · for Know-Center (€120k for Social Computing) · researcher',
    url: 'https://project.gotriple.eu/',
  },
  {
    name: 'Marshall Plan Fellowship',
    amount: null,
    kind: 'fellowship',
    years: '2018',
    detail: 'Individual research grant for a visiting stay at UCLA, Los Angeles',
  },
  {
    name: 'Data Market Austria',
    amount: '€286,000',
    kind: 'project grant',
    years: '2015',
    detail: 'IKT der Zukunft · secured for Know-Center as technology contributor for the recommender-based brokerage platform',
  },
] as const;

/** Awards and honours. These live on /cv, not the landing page. */
export const awards = [
  { year: 2022, name: 'Mind-the-gap gender and diversity award', detail: 'Graz University of Technology, for research on fairness in AI and bias in recommender systems.' },
  { year: 2018, name: 'Marshall Plan Fellowship', detail: 'Visiting scholar fellowship at the University of California, Los Angeles.' },
  { year: 2016, name: 'Travel grant', detail: "27th ACM Conference on Hypertext and Social Media (HT'16), Halifax, Canada." },
  { year: 2015, name: 'Best demo honourable mention', detail: "15th International Conference on Knowledge Technologies and Data-Driven Business (i-KNOW'15), Graz." },
  { year: 2014, name: 'Best poster award', detail: "25th ACM Conference on Hypertext and Social Media (HT'14), Santiago, Chile." },
  { year: 2012, name: 'Erasmus scholarship', detail: 'Final master year at Karlsruhe Institute of Technology.' },
] as const;

export const languages = [
  { name: 'Croatian', level: 'native' },
  { name: 'English', level: 'C1' },
  { name: 'German', level: 'C1' },
  { name: 'Russian', level: 'A1' },
] as const;

/**
 * Infobip's dark/bright colour pairs, one per area. `ink` is the tile
 * background, `glow` the icon and name on top of it.
 *
 * tools/air/compose.html hard-codes the same four pairs, because it is a
 * standalone HTML file rendered by headless Chrome and cannot import TypeScript.
 * Change a value here and change it there too, or the carousel and the
 * generated image will disagree.
 */
export const airPalettes = {
  pink: { ink: '#32232F', glow: '#FFA8EB' },
  green: { ink: '#053133', glow: '#CBEA99' },
  blue: { ink: '#17283A', glow: '#9EB2FF' },
  brand: { ink: '#2D2C2B', glow: '#FC6423' },
} as const;

export type AirPalette = keyof typeof airPalettes;

/**
 * The eight AIR research areas, matching research.infobip.com/research.
 * The landing page shows these as one generated image and names them only;
 * /air walks through them one at a time in AirCarousel.astro.
 * The order and the palettes here match the image (tools/air/compose.html).
 *
 * `icon` is a filename in public/icons/air/ rather than something derived from
 * the slug, because the generative-models icon is filed under a different name
 * than its area.
 *
 * `focus` holds the phrases the carousel emphasises — the payoff of the
 * sentence, not the topic, which the tile title already gives. Each one must
 * appear verbatim in `summary`; the build fails if it does not.
 */
export const researchAreas = [
  {
    name: 'Human-AI Collaboration',
    slug: 'human-ai-collaboration',
    icon: 'human-ai-collaboration.svg',
    palette: 'pink',
    summary:
      'People trust AI communication systems unevenly. We study where that trust forms, and what it means for transparent, predictable design.',
    focus: ['where that trust forms', 'transparent, predictable design'],
  },
  {
    name: 'Trustworthy AI',
    slug: 'trustworthy-ai',
    icon: 'trustworthy-ai.svg',
    palette: 'green',
    summary:
      'Fairness, transparency and accountability in AI-driven communication, with evaluation and explainability built for real-world deployment.',
    focus: ['Fairness, transparency and accountability', 'real-world deployment'],
  },
  {
    name: 'Conversational AI',
    slug: 'conversational-ai',
    icon: 'conversational-ai.svg',
    palette: 'blue',
    summary:
      'Most systems respond without resolving. We work on context, personalization and multimodal signals across text, voice and vision.',
    focus: ['respond without resolving', 'multimodal signals'],
  },
  {
    name: 'AI-powered Communication',
    slug: 'ai-powered-communication',
    icon: 'ai-powered-communication.svg',
    palette: 'brand',
    summary:
      'Intelligent routing, adaptive orchestration and predictive network management that reduce latency and operational overhead, and recover from failures automatically.',
    focus: ['reduce latency and operational overhead'],
  },
  {
    name: 'Fraud Detection',
    slug: 'fraud-detection',
    icon: 'fraud-detection.svg',
    palette: 'green',
    summary:
      'Anomaly detection, behavioural modelling and prediction to catch fraud and malicious activity across communication channels, in real time and at scale.',
    focus: ['in real time and at scale'],
  },
  {
    name: 'Spam Filtering',
    slug: 'spam-filtering',
    icon: 'spam-filtering.svg',
    palette: 'blue',
    summary:
      'Spam shifts faster than the models that catch it. Detection across text, images and voice, at the latency high traffic demands.',
    focus: ['shifts faster than the models that catch it'],
  },
  {
    name: 'Voice AI',
    slug: 'voice-ai',
    icon: 'voice-ai.svg',
    palette: 'brand',
    summary:
      'Speech enhancement, noise suppression, compression and unbiased voice processing, so voice quality holds up under real network conditions.',
    focus: ['holds up under real network conditions'],
  },
  {
    name: 'Generative Models',
    slug: 'generative-models',
    icon: 'special-generative-models.svg',
    palette: 'pink',
    summary:
      'Domain-specific generative architectures for communication platforms, prioritising privacy, efficiency and operational control, including lightweight and privacy-preserving deployment.',
    focus: ['privacy, efficiency and operational control'],
  },
] as const;

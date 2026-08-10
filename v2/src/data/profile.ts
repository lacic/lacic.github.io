/**
 * Singleton site data: identity, career, education, funding, links.
 *
 * Lists that grow (publications, talks, projects, service, posts) are content
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
    lines: ['I lead Team AI Research', 'at Infobip, building AI for', 'communication at global scale'],
    coda: '— and finding out what survives production.',
  },

  /** The working note in the hero margin. */
  workingNote:
    'Most of what we try does not work. This site is where I write down which parts did, and why the difference was rarely the model.',

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
        detail: 'Founded and lead Team AI Research, focusing on generative AI and the impact of LLMs.',
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
      {
        years: '2018',
        title: 'Visiting researcher, UCLA Computer Science',
        detail: 'Marshall Plan Fellowship — session-based recommendation.',
        concurrent: true,
        tag: 'visiting',
      },
    ],
  },
  {
    org: 'Graz University of Technology',
    place: 'Graz',
    span: '2013—2016',
    url: 'https://www.tugraz.at/en/home/',
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
 */
export const education = [
  {
    degree: 'PhD, Computer Science',
    distinction: 'with distinction',
    institution: 'Graz University of Technology',
    place: 'Graz',
    year: 2022,
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
 * `amount` is only set where the figure is public.
 */
export const funding = [
  {
    name: 'IPCEI-CIS',
    amount: null,
    kind: 'EU programme',
    years: '2026 —',
    detail: 'Multi-country EU research project on cloud and edge infrastructure · Infobip research lead',
  },
  {
    name: 'EDIH Adria',
    amount: null,
    kind: 'EU programme',
    years: '2023 —',
    detail: 'European Digital Innovation Hub for AI and high-performance computing · partner',
  },
  {
    name: 'Data Market Austria',
    amount: '€286,000',
    kind: 'project grant',
    years: '2015',
    detail: 'IKT der Zukunft · secured for Know-Center as technology contributor for the recommender-based brokerage platform',
  },
  {
    name: 'Marshall Plan Fellowship',
    amount: null,
    kind: 'fellowship',
    years: '2018',
    detail: 'Individual research grant for a visiting stay at UCLA, Los Angeles',
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
 * The eight AIR research areas, matching research.infobip.com/research.
 * The landing page shows these as one generated image and names them only.
 * The order here matches the order in the image (tools/air/compose.html).
 */
export const researchAreas = [
  {
    name: 'Human-AI Collaboration',
    slug: 'human-ai-collaboration',
    summary:
      'How people work with AI-powered communication systems in practice: where trust forms, how individual differences and system explanations shape confidence, and what that implies for transparent and predictable design.',
  },
  {
    name: 'Trustworthy AI',
    slug: 'trustworthy-ai',
    summary:
      'Fairness, transparency and accountability in AI-driven communication, using evaluation and explainability techniques that survive real-world settings rather than only benchmarks.',
  },
  {
    name: 'Conversational AI',
    slug: 'conversational-ai',
    summary:
      'Context awareness, personalization and multimodal interaction across text, voice and visual signals, so conversations resolve rather than merely respond.',
  },
  {
    name: 'AI-powered Communication',
    slug: 'ai-powered-communication',
    summary:
      'Intelligent routing, adaptive orchestration and predictive network management that reduce latency and operational overhead, and recover from failures automatically.',
  },
  {
    name: 'Fraud Detection',
    slug: 'fraud-detection',
    summary:
      'Anomaly detection, behavioural modelling and prediction to catch fraud and malicious activity across communication channels, in real time and at scale.',
  },
  {
    name: 'Spam Filtering',
    slug: 'spam-filtering',
    summary:
      'Detecting spam and harmful content across text, images and voice under topic drift and distribution shift, with the accuracy and latency a high-traffic network demands.',
  },
  {
    name: 'Voice AI',
    slug: 'voice-ai',
    summary:
      'Speech enhancement, noise suppression, compression and unbiased voice processing, so voice quality holds up under real network conditions.',
  },
  {
    name: 'Generative Models',
    slug: 'generative-models',
    summary:
      'Domain-specific generative architectures for communication platforms, prioritising privacy, efficiency and operational control, including lightweight and privacy-preserving deployment.',
  },
] as const;

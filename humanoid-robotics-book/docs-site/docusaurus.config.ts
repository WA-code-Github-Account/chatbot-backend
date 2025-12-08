// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'A Comprehensive Guide to Building Intelligent Humanoid Systems',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://your-site.vercel.app',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For Vercel deployment, this should be '/'
  baseUrl: '/',

  // GitHub pages deployment config.
  organizationName: 'aziza-siddiqui', // Your GitHub username
  projectName: 'humanoid-robotics-book', // Your repo name

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          routeBasePath: '/',
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: 'Humanoid Robotics',
        logo: {
          alt: 'Humanoid Robotics Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'doc',
            docId: 'intro',
            position: 'left',
            label: '📚 Book',
          },
          {
            to: '/part1',
            label: 'Part 1',
            position: 'left',
          },
          {
            to: '/part2',
            label: 'Part 2',
            position: 'left',
          },
          {
            to: '/part3',
            label: 'Part 3',
            position: 'left',
          },
          {
            to: '/part4',
            label: 'Part 4',
            position: 'left',
          },
          {
            href: 'https://github.com/yourusername/humanoid-robotics-book',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Book Sections',
            items: [
              {
                label: 'Introduction',
                to: '/',
              },
              {
                label: 'Part 1: Foundations',
                to: '/part1',
              },
              {
                label: 'Part 2: Core Technologies',
                to: '/part2',
              },
              {
                label: 'Part 3: Advanced Topics',
                to: '/part3',
              },
            ],
          },
          {
            title: 'More Chapters',
            items: [
              {
                label: 'Part 4: Applications',
                to: '/part4',
              },
              {
                label: 'Chapter 1: Introduction',
                to: '/chapter1',
              },
              {
                label: 'Chapter 20: Conclusion',
                to: '/chapter20',
              },
            ],
          },
          {
            title: 'Connect',
            items: [
              {
                label: 'GitHub Repository',
                href: 'https://github.com/yourusername/humanoid-robotics-book',
              },
              {
                label: 'GIAIC Official',
                href: 'https://www.giaic.com',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Aziza Siddiqui | GIAIC Student. Built with Docusaurus.`,
      },
    
    }),
};

module.exports = config;

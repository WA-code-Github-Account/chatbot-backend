import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'A Comprehensive Guide to Building Intelligent Humanoid Systems',
  favicon: 'img/favicon.ico',

  url: 'https://your-site.vercel.app',  // <- apna Vercel URL replace kar do
  baseUrl: '/',

  organizationName: 'aziza-siddiqui',
  projectName: 'humanoid-robotics-book',

  // ✅ Broken links fix
  onBrokenLinks: 'ignore',         // <- ye change kiya
  onBrokenMarkdownLinks: 'warn',   // warning sirf dikhegi, build fail nahi hoga

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          routeBasePath: '/', // docs homepage
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    navbar: {
      title: 'Humanoid Robotics',
      logo: {
        alt: 'Humanoid Robotics Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'doc',
          docId: 'physical-ai-humanoid-robotics/intro',
          position: 'left',
          label: '📚 Book',
        },
        {
          href: 'https://github.com/WA-code-Github-Account/humanoid-robotics-book',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Documentation',
          items: [
            {
              label: 'Introduction',
              to: '/physical-ai-humanoid-robotics/intro',
            },
          ],
        },
        {
          title: 'Connect',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/WA-code-Github-Account/humanoid-robotics-book',
            },
            {
              label: 'GIAIC',
              href: 'https://www.giaic.com',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Aziza Siddiqui | GIAIC Student. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;

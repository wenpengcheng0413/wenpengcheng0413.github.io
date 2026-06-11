import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const projects = defineCollection({
  loader: glob({ pattern: '**/*.mdx', base: './src/content/projects' }),
  schema: z.object({
    title: z.string(),
    subtitle: z.string(),
    description: z.string(),
    grade: z.enum(['S', 'A', 'B', 'C']),
    category: z.enum([
      '环境科学', 'AI开发', '桌面工具', 'Web应用', '移动开发', '游戏', '内容创作',
    ]),
    techStack: z.array(z.string()),
    completionRate: z.number().min(0).max(100),
    featured: z.boolean().default(false),
    github: z.string().url().optional(),
    demoUrl: z.string().url().optional(),
    coverImage: z.string().optional(),
    sortOrder: z.number().default(99),
    publishedAt: z.date(),
    updatedAt: z.date().optional(),
  }),
});

const blog = defineCollection({
  loader: glob({ pattern: '**/*.mdx', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    category: z.string(),
    tags: z.array(z.string()),
    maturity: z.enum(['seedling', 'budding', 'evergreen']).default('seedling'),
    publishedAt: z.date(),
    updatedAt: z.date().optional(),
    draft: z.boolean().default(false),
  }),
});

const garden = defineCollection({
  loader: glob({ pattern: '**/*.mdx', base: './src/content/garden' }),
  schema: z.object({
    date: z.date(),
    title: z.string(),
    description: z.string().optional(),
    category: z.enum([
      'milestone', 'project-log', 'review', 'reflection',
      'academic', 'creative', 'hobby', 'daily',
    ]),
    tags: z.array(z.string()).default([]),
    bilibili_url: z.string().optional(),
    images: z.array(z.string()).default([]),
    mood: z.enum(['sunny', 'cloudy', 'rainy']).optional(),
  }),
});

export const collections = { projects, blog, garden };

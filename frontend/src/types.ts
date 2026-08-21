export interface Task { id: number; title: string; completed: boolean; priority: 'low' | 'medium' | 'high'; tags: Tag[] }
export interface Tag { id: number; name: string }
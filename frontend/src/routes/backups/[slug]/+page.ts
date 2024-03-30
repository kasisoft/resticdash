import { backupinfosStore } from '$lib/stores.svelte';
import { error } from '@sveltejs/kit';

export const ssr = false;

export async function load({ params }) {
    const list = backupinfosStore.value.filter(v => v.name === params.slug);
    if (list.length == 1) {
        return {
            info: list[0],
            slug: params.slug
        };
    }
    throw error(404);
}

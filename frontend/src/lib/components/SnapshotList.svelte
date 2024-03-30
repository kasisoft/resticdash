<script lang="ts">

    import { _ } from 'svelte-i18n';

    import type { SnapshotInfo } from '$lib/types';
    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    const { snapshots } = $props<{ snapshots: SnapshotInfo[] }>();

    let selectedRow: number | null = $state<number|null>(null);

    function selectRow(row: number) {
        selectedRow = row;
        dispatch('select', {
            message: snapshots[row]
        });
    }

</script>

<div class="bg-primary-300 dark:bg-primary-200">
    <table class="bv dark:bg-primary-200">
        <thead>
            <tr>
                <th>{$_('backup.date')}</th>
                <th>{$_('backup.time')}</th>
                <th>{$_('backup.short_id')}</th>
            </tr>
        </thead>
        <tbody>
            {#each snapshots as snapshot, j}
            <tr class="hover:bg-primary-400" class:selected={j == selectedRow} on:click={() => selectRow(j)}>
                <td>{snapshot.time.toLocaleDateString()}</td>
                <td>{snapshot.time.toLocaleTimeString()}</td>
                <td>{snapshot.short_id}</td>
            </tr>
            {/each}
        </tbody>
    </table>
</div>

<style lang="postcss">
    div {
        padding: 1rem;
        height: 100%;
        width: 32rem;
    }
    th {
        text-align: left;
        width: 10rem;
    }
    .selected {
        @apply bg-primary-400;
    }
    /*
     * @todo [27-MAR-2024:KASI]  Matching via classes doesn't seem to work right. Figure out why?
     * :global etc didn't work or I made an error!
     */
    .bv {
        color: theme('colors.primary.700');
    }
</style>

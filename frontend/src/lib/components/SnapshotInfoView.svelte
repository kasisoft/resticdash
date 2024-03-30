<script lang="ts">

    import type { SnapshotInfo } from '$lib/types';

    let { info } = $props<{ snapshotInfo: SnapshotInfo }>();

</script>

<div class="bg-primary-300 dark:bg-primary-200 text-primary-700">
    {#if info}
        <div class="infos">
            <span class="font-semibold">ID:</span><span>{info.id}</span>
            <span class="font-semibold">Short ID:</span><span>{info.short_id}</span>
            <span class="font-semibold">Time:</span><span>{info.time}</span>
            <span class="font-semibold">Username:</span><span>{info.username}</span>
            <span class="font-semibold">Paths:</span><span>{info.paths}</span>
            <span class="font-semibold">UID:</span><span>{info.uid}</span>
            <span class="font-semibold">GID:</span><span>{info.gid}</span>
            <span class="font-semibold">Hostname:</span><span>{info.hostname}</span>
            <span class="font-semibold">Tree:</span><span>{info.tree}</span>
        </div>
    {/if}
</div>

<style lang="postcss">
    div {
        padding: 1rem;
    }
    .infos {
        display: grid;
        grid-template-columns: max-content 1fr;
        column-gap: 1rem;
    }
</style>

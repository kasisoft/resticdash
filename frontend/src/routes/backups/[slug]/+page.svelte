<script lang="ts">

    import SnapshotInfoView from '$lib/components/SnapshotInfoView.svelte';
    import SnapshotList from '$lib/components/SnapshotList.svelte';
    import type { BackupInfos, SnapshotInfo } from '$lib/types.js';

    let { data } = $props();

    const info: BackupInfos = data.info;

    let selectedSnapshot = $state<SnapshotInfo | null>(null);

    function handleSelect(event) {
        const snapshot: SnapshotInfo = event.detail.message;
        selectedSnapshot = snapshot;
    }

</script>

{#if info}
<div>
    <SnapshotList on:select={handleSelect} snapshots={info.snapshots} />
    <SnapshotInfoView info={selectedSnapshot} />
</div>
{/if}


<style lang="postcss">
    div {
        padding-top: var(--outer-padding);
        padding-bottom: var(--outer-padding);
        display: grid;
        grid-template-columns: auto 1fr;
        column-gap: 1rem;
        row-gap: 1rem;
    }
</style>


<script lang="ts">

    import SnapshotList from '$lib/components/SnapshotList.svelte';
    import type { BackupInfos, SnapshotInfo } from '$lib/types.js';

    let { data } = $props();

    const info: BackupInfos = data.info;

    function handleSelect(event) {
        const snapshot: SnapshotInfo = event.detail.message;
        console.log(JSON.stringify(snapshot));
    }

</script>

{#if info}
<div>
    <SnapshotList on:select={handleSelect} snapshots={info.snapshots} />
</div>
{/if}


<style lang="postcss">
    div {
        padding-top: var(--outer-padding);
        padding-bottom: var(--outer-padding);
    }
</style>


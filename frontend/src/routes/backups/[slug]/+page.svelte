<script lang="ts">

    import BackupInfoView from '$lib/components/BackupInfoView.svelte';
    import type { BackupInfos } from '$lib/types.js';

    let { data } = $props();

    const info: BackupInfos = data.info;

</script>

<div>
    {#if info}
        <BackupInfoView backupInfo={info} />
    {/if}
</div>


<style lang="postcss">
    div {
        padding-top: var(--outer-padding);
        padding-bottom: var(--outer-padding);
    }
</style>


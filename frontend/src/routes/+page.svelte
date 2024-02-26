<script lang="ts">
    import { backupinfosStore } from '$lib/stores.svelte';
    import BackupInfoView from '$lib/components/BackupInfoView.svelte';
    import AutoReload from '$lib/components/AutoReload.svelte';
</script>

<div class="full-width">
    <AutoReload />
    <div class="backupinfo-views">
        {#key backupinfosStore.value}
        {#each backupinfosStore.value as record}
            <BackupInfoView backupInfo={record}/>
        {/each}
        {/key}
    </div>
</div>

<style lang="postcss">
    .backupinfo-views {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        justify-content: center;
        padding: var(--outer-padding);
    }
</style>

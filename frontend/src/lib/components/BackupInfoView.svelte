<script lang="ts">

    import { Card } from 'svelte-5-ui-lib';
    import { _ } from 'svelte-i18n';

    import type { BackupInfos, SnapshotInfo } from '$lib/types';

    let { backupInfo } = $props<{ backupInfo: BackupInfos }>();

    let snapshotInfos: SnapshotInfo[] = [];

    let failed: boolean = false;
    if (backupInfo) {
        if (backupInfo.snapshots.length > 0) {
            const lastBackup = backupInfo.snapshots[backupInfo.snapshots.length - 1].time;
            const now        = new Date();
            const millis     = now.getTime() - lastBackup.getTime();
            const seconds    = millis / 1000;
            failed           = seconds >= backupInfo.backup_fail_delay;
            snapshotInfos.push(backupInfo.snapshots[backupInfo.snapshots.length - 1]);
            snapshotInfos.push(backupInfo.snapshots[0]);
        } else {
            // no snapshots is considered to be an error
            failed = true;
        }
    }

    const colorClass = failed ? "bg-red-200 dark:bg-red-200" : "bg-green-300 dark:bg-green-300";

</script>

<Card href="./backups/{backupInfo.name}" class="{colorClass} border-primary-500 dark:border-primary-200 hover:bg-gray-100 dark:hover:bg-gray-100">
    <h5 class="bv mb-2 text-2xl font-bold tracking-tight">{backupInfo.name}</h5>
    <p class="bv font-semibold mb-2 ">{$_('backup.snapshots')}: {backupInfo.snapshots.length}</p>
    <table class="bv">
        <thead>
            <tr>
                <th>{$_('backup.date')}</th>
                <th>{$_('backup.time')}</th>
                <th>{$_('backup.short_id')}</th>
            </tr>
        </thead>
        <tbody>
            {#each snapshotInfos as snapshot, j}
            <tr>
                <td>{snapshot.time.toLocaleDateString()}</td>
                <td>{snapshot.time.toLocaleTimeString()}</td>
                <td>{snapshot.short_id}</td>
            </tr>
            {/each}
        </tbody>
    </table>
</Card>

<style lang="postcss">
    th {
        text-align: left;
        width: 10rem;
    }
    /*
     * @todo [27-MAR-2024:KASI]  Matching via classes doesn't seem to work right. Figure out why?
     * :global etc didn't work or I made an error!
     */
    .bv {
        color: theme('colors.primary.700');
    }
</style>

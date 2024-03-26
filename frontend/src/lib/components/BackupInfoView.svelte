<script lang="ts">

    import type { BackupInfos, SnapshotInfo } from '$lib/types';
    import { _ } from 'svelte-i18n';

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
            snapshotInfos.push(backupInfo.snapshots[0]);
            snapshotInfos.push(backupInfo.snapshots[backupInfo.snapshots.length - 1]);
        } else {
            // no snapshots is considered to be an error
            failed = true;
        }
    }

    const colorClass = failed ? "bg-red-200" : "bg-green-200";

</script>

<div>
    <a href="#" class="{colorClass} block max-w-sm p-6 border border-gray-200 rounded-lg shadow hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700">
        <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">{backupInfo.name}</h5>
        <p class="font-normal mb-2 text-gray-700 dark:text-gray-400">{$_('backup.snapshots')}: {backupInfo.snapshots.length}</p>
        <table>
            <thead>
                <tr>
                    <th class="date">{$_('backup.date')}</th>
                    <th class="time">{$_('backup.time')}</th>
                    <th class="shortid">{$_('backup.short_id')}</th>
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
    </a>
</div>

<style lang="postcss">
    div {
        height: 12rem;
        > a {
            height: 100%;
        }
    }
    .date {
        width: 10rem;
        text-align: left;
    }
    .time {
        width: 9rem;
        text-align: left;
    }
    .shortid {
        width: 9rem;
        text-align: left;
    }


</style>

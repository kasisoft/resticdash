import { ark, arrayOf, type } from 'arktype';

export const FrontendCfgDef = type({
    "reload": "number",
    "timeout": "number"
});

export type FrontendCfg = typeof FrontendCfgDef.infer;

export const DEFAULT_FRONTENDCFG: FrontendCfg = {
    reload: 60,
    timeout: 10
};

export const SnapshotInfoDef = type({
    "id": "string",
    "short_id": "7<string<9",
    "time": ["string", "|>", ark.parsedDate],
    "gid": "string|null",
    "uid": "string|null",
    "hostname": "string|null",
    "tree": "string|null",
    "username": "string|null",
    "paths": "string[]",
});

export type SnapshotInfo = typeof SnapshotInfoDef.infer;

export const BackupInfosDef = type({
    "name": "0<string<100",
    "backup_fail_delay": "0<integer<=1000000000",
    "snapshots": arrayOf(SnapshotInfoDef),   // oldest = 0, newest = length - 1
});

export type BackupInfos = typeof BackupInfosDef.infer;

export const BackupInfosListDef = arrayOf(BackupInfosDef);

export type BackupInfosList = typeof BackupInfosListDef.infer;

export enum ApplicationState {

    Loading, // Fetching is underway
    Display, // Progress is running down until the next reload

}

import {  BackupInfosListDef, FrontendCfgDef, type BackupInfosList, type FrontendCfg } from '$lib/types';
import axios, { type AxiosResponse } from 'axios';
import type { CheckResult } from 'arktype/internal/traverse/traverse.js';

function isAbsolute(url: string): boolean {
    if (url) {
        return url.startsWith('http:') || url.startsWith('https:');
    }
    return false;
}

function removeStart(input: string, start: string): string {
    if (input && input.startsWith(start)) {
        return input.substring(start.length);
    }
    return input;
}

function removeEnd(input: string, end: string): string {
    if (input && input.endsWith(end)) {
        return input.substring(0, input.length - end.length);
    }
    return input;
}

type ProcessPayload<T> = (payload: unknown) => CheckResult<T>;

export type ClientErrorHandler = (error: string) => void;

export class ResticDashClient {

    /* baseUrl: string; */
    timeoutInSeconds: number;
    errorHandler: ClientErrorHandler;
    timeoutmsg: string;

    constructor(timeoutInSeconds: number = 90, errorHandler?: ClientErrorHandler, timeoutmsg?: string) {

        this.getBaseUrl = this.getBaseUrl.bind(this);
        this.getBackendUrl = this.getBackendUrl.bind(this);
        this.axiosGet = this.axiosGet.bind(this);
        this.getConfig = this.getConfig.bind(this);
        this.getRestic = this.getRestic.bind(this);
        this.logError = this.logError.bind(this);

        /* this.baseUrl = this.getBaseUrl(); */
        this.timeoutInSeconds = timeoutInSeconds;
        this.errorHandler = errorHandler ?? this.logError;
        this.timeoutmsg = timeoutmsg ?? "Timeout";

    }

    logError(error: string) {
        console.error(error);
    }

    getBaseUrl(): string {
        const url: URL = new URL(window.location.href);
        let result: string = url.protocol + '//' + url.hostname;
        if (url.port && url.port.length > 0) {
            result = result + ":" + url.port;
        }
        const path_segments = removeStart(url.pathname, '/').split('/');
        if (path_segments.length > 0) {
            const first = path_segments[0];
            if (first.endsWith('.html') ||  first.endsWith('.htm')) {
                // it's a page so there's no context path
            } else {
                result = result + '/' + first;
            }
        }
        return result;
    }

    getBackendUrl(endpoint: string): string {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        if (isAbsolute(backendUrl)) {
            return removeEnd(backendUrl, '/') + endpoint;
        } else {
            return this.getBaseUrl() + endpoint;
        }
    }
    
    async axiosGet<T>(endpoint: string, process: ProcessPayload<T>): Promise<T | undefined> {
        const timeout = this.timeoutInSeconds * 1000;
        try {
            const url = this.getBackendUrl(endpoint);
            const result = await axios.get(
                url,
                { headers: { Accept: 'application/json' }, timeout: timeout }
            );
            const { data, status } = result as AxiosResponse<T>;
            if (status === 200) {
                const parsed = process(data);
                if (parsed.problems) {
                    this.errorHandler(JSON.stringify(parsed.problems))
                } else {
                    return new Promise<T>((resolve) => resolve(parsed.data));
                }
            }  else {
                this.errorHandler(JSON.stringify(data));
            }
        } catch (err) {
            if (axios.isAxiosError(err)) {
                if ("ECONNABORTED" == err.code) {
                    this.errorHandler(this.timeoutmsg);
                } else {
                    this.errorHandler(err.message);
                }
            } else {
                this.errorHandler(JSON.stringify(err));
            }
        }
        return new Promise<undefined>((resolve) => resolve(undefined));
    }

    async getConfig(): Promise<FrontendCfg | undefined> {
        return this.axiosGet<FrontendCfg>("/api/config", FrontendCfgDef);
    }
    
    async getRestic(): Promise<BackupInfosList | undefined> {
        return this.axiosGet<BackupInfosList>("/api/restic", BackupInfosListDef);
    }

} /* ENDCLASS */

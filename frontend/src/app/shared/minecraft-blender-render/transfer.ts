import { HttpEvent, HttpResponse, HttpEventType, HttpProgressEvent } from "@angular/common/http";

export interface Transfer {
    progress: number,
    state: 'PENDING' | 'UPLOAD_PROGRESS' | 'UPLOAD_DONE' | 'DOWNLOAD_PROGRESS' | 'DOWNLOAD_DONE' | 'DONE',
    event?: any,
};

export const initialState: Transfer = { state: 'PENDING', progress: 0 };

export function isHttpResponse<T>(event: HttpEvent<T>): event is HttpResponse<T> {
    return event.type === HttpEventType.Response
};

export function isHttpUploadProgressEvent(event: HttpEvent<unknown>): event is HttpProgressEvent {
    return event.type === HttpEventType.UploadProgress;
};

export function isHttpDownloadProgressEvent(event: HttpEvent<unknown>): event is HttpProgressEvent {
    return event.type === HttpEventType.DownloadProgress;
};

export function isHttpProgressEvent(event: HttpEvent<unknown>): event is HttpProgressEvent {
    return isHttpUploadProgressEvent(event) || isHttpDownloadProgressEvent(event);
};

export function progressToState(progress: number, isUpload: boolean): 'UPLOAD_PROGRESS' | 'UPLOAD_DONE' | 'DOWNLOAD_PROGRESS' | 'DOWNLOAD_DONE' {
    if (progress < 1) {
        if (isUpload) {
            return'UPLOAD_PROGRESS';
        }
        return 'DOWNLOAD_PROGRESS';
    }
    if (isUpload) {
        return'UPLOAD_DONE';
    }
    return 'DOWNLOAD_DONE';
}

export function calculateState(upload: Transfer, event: HttpEvent<unknown>): Transfer {
    if (isHttpProgressEvent(event)) {
        const progress = event.total ? event.loaded / event.total : upload.progress;
        return {
            progress: progress,
            state: progressToState(progress, isHttpUploadProgressEvent(event)),
            event: event,
        };
    }
    if (isHttpResponse(event)) {
        return {
            progress: 1,
            state: 'DONE',
            event: event,
        };
    }
    return upload;
};

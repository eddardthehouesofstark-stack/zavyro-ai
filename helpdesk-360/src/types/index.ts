export type Role='employee'|'technician'
export type Status='New'|'Assigned'|'In Progress'|'Waiting for Employee'|'Resolved'|'Closed'
export type Priority='Low'|'Medium'|'High'|'Critical'
export const STATUSES:Status[]=['New','Assigned','In Progress','Waiting for Employee','Resolved','Closed']
export interface User{id:string;name:string;email:string;role:Role}
export interface Ticket{id:string;title:string;description:string;status:Status;priority:Priority;category:string;employee?:string;department?:string;device?:string;updatedAt:string;slaDueAt?:string}
export interface Message{id:string;author:string;kind:'employee'|'technician'|'internal';body:string;createdAt:string}
export interface AiAnalysis{category:string;priority:Priority;summary:string}
export interface AiAssist{summary:string;solution:string;draftReply:string;steps:string[];articles:{id:string;title:string}[]}

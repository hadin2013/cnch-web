import type { SchoolGroup } from '$lib/schemas/schoolGroup.schema';
import type { Student } from '$lib/schemas/student.schema';
import { env } from '$env/dynamic/public';

const API_BASE_URL = env.PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000/user';
const API_ROOT = API_BASE_URL.replace(/\/user\/?$/, '');

// ---------------------------------------------------------------------------
// Types shared with the profile/admin UI
// ---------------------------------------------------------------------------

export interface ApiUser {
	id: number;
	username: string;
	first_name: string;
	last_name: string;
	email: string;
	phone_number: string;
	national_id: string | null;
	date_of_birth: string | null;
	address: string | null;
	role: 'normal' | 'mentor' | 'admin';
	is_email_activated: boolean;
	user_credit: number;
	created_at: string;
}

export interface ProfileData {
	user: ApiUser;
	group: (SchoolGroupResponse & { students: StudentResponse[] }) | null;
	student: StudentResponse | null;
	tickets: Ticket[];
}

export interface Ticket {
	id: number;
	user: number;
	user_name: string;
	title: string;
	message: string;
	created_at: string;
	resolved: boolean;
}

export interface AdminUserRow {
	id: number;
	username: string;
	first_name: string;
	last_name: string;
	email: string;
	phone_number: string;
	national_id: string | null;
	role: 'normal' | 'mentor' | 'admin';
	student_group: number | null;
	is_student: boolean;
	created_at: string;
}

export interface AdminGroupRow {
	id: number;
	group_name: string;
	province: string;
	city: string;
	school_name: string;
	school_phone: string;
	organizer: number | null;
	organizer_name: string | null;
	student_count: number;
	finalized: boolean;
}

/** Turn DRF error payloads ({field: [msgs]} | {detail}) into one Persian message. */
function extractApiError(error: unknown): string | undefined {
	if (!error) return undefined;
	if (typeof error === 'string') return error;
	if (typeof error !== 'object') return String(error);
	const payload = error as Record<string, unknown>;
	if (payload.detail) {
		return Array.isArray(payload.detail)
			? payload.detail.map((item) => String(item)).join('، ')
			: String(payload.detail);
	}
	const msgs: string[] = [];
	for (const [field, val] of Object.entries(payload)) {
		if (Array.isArray(val)) msgs.push(...val.map(String));
		else msgs.push(`${field}: ${String(val)}`);
	}
	return msgs.join('، ');
}

async function authFetch(
	token: string | null,
	path: string,
	init: RequestInit = {}
): Promise<Response> {
	const headers = new Headers(init.headers);
	headers.set('Content-Type', 'application/json');
	if (token) headers.set('Authorization', `Bearer ${token}`);
	const response = await fetch(API_ROOT + path, { ...init, headers });
	if (!response.ok) {
		const error = await response.json().catch(() => ({}));
		throw new Error(extractApiError(error) || 'خطا در ارتباط با سرور');
	}
	return response;
}

export interface SchoolGroupResponse {
	id: number;
	group_name: string;
	province: string;
	city: string;
	school_name: string;
	school_phone: string;
}

export interface StudentResponse {
	id: number;
	school_group: number;
	first_name: string;
	last_name: string;
	national_id: string;
	phone_number: string;
	grade: string;
	major: string;
}

export async function createSchoolGroup(
	data: SchoolGroup,
	token?: string | null
): Promise<SchoolGroupResponse> {
	const response = await fetch(`${API_BASE_URL}/groups/`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			...(token ? { Authorization: `Bearer ${token}` } : {})
		},
		body: JSON.stringify(data)
	});

	if (!response.ok) {
		const error = await response.json().catch(() => ({}));
		throw new Error(extractApiError(error) || 'خطا در ثبت اطلاعات گروه مدرسه');
	}

	return response.json();
}

export async function createStudent(
	data: Student & { school_group: number },
	token?: string | null
): Promise<StudentResponse> {
	const response = await fetch(`${API_BASE_URL}/students/`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			...(token ? { Authorization: `Bearer ${token}` } : {})
		},
		body: JSON.stringify(data)
	});

	if (!response.ok) {
		const error = await response.json().catch(() => ({}));
		throw new Error(extractApiError(error) || 'خطا در ثبت اطلاعات دانش‌آموز');
	}

	return response.json();
}

export async function updateStudent(
	studentId: number,
	data: Partial<Student>
): Promise<StudentResponse> {
	const response = await fetch(`${API_BASE_URL}/students/${studentId}/`, {
		method: 'PATCH',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(data)
	});

	if (!response.ok) {
		const error = await response.json().catch(() => ({}));
		throw new Error(error.message || 'خطا در ویرایش اطلاعات دانش‌آموز');
	}

	return response.json();
}

export async function getGroupDashboard(groupId: number): Promise<any> {
	const response = await fetch(`${API_BASE_URL}/groups/${groupId}/`);

	if (!response.ok) {
		throw new Error('خطا در دریافت اطلاعات گروه');
	}

	return response.json();
}

// ---------------------------------------------------------------------------
// Auth (signup / login)
// ---------------------------------------------------------------------------

export async function signup(data: {
	email: string;
	password: string;
	first_name?: string;
	last_name?: string;
	phone_number?: string;
	national_id?: string;
}): Promise<ApiUser> {
	const response = await authFetch(null, '/user/signup/', {
		method: 'POST',
		body: JSON.stringify(data)
	});
	return response.json();
}

export async function login(
	email: string,
	password: string
): Promise<{ access: string; refresh: string }> {
	const response = await authFetch(null, '/api/token/', {
		method: 'POST',
		body: JSON.stringify({ username: email, password })
	});
	return response.json();
}

// ---------------------------------------------------------------------------
// Profile
// ---------------------------------------------------------------------------

export async function getProfile(token: string | null): Promise<ProfileData> {
	const response = await authFetch(token, '/user/profile/');
	return response.json();
}

export async function updateProfile(
	token: string | null,
	data: Partial<
		Pick<
			ApiUser,
			'first_name' | 'last_name' | 'email' | 'phone_number' | 'date_of_birth' | 'address'
		>
	>
): Promise<ApiUser> {
	const response = await authFetch(token, '/user/profile/', {
		method: 'PATCH',
		body: JSON.stringify(data)
	});
	return response.json();
}

export async function changePassword(
	token: string | null,
	data: { old_password: string; new_password: string }
): Promise<{ detail: string }> {
	const response = await authFetch(token, '/user/profile/change-password/', {
		method: 'POST',
		body: JSON.stringify(data)
	});
	return response.json();
}

export async function createTicket(
	token: string | null,
	data: { title: string; message: string }
): Promise<Ticket> {
	const response = await authFetch(token, '/user/profile/tickets/', {
		method: 'POST',
		body: JSON.stringify(data)
	});
	return response.json();
}

// ---------------------------------------------------------------------------
// Admin panel
// ---------------------------------------------------------------------------

export async function adminListUsers(
	token: string | null,
	params: { q?: string; role?: string } = {}
): Promise<AdminUserRow[]> {
	const search = new URLSearchParams();
	if (params.q) search.set('q', params.q);
	if (params.role) search.set('role', params.role);
	const qs = search.toString();
	const response = await authFetch(token, `/user/admin/users/${qs ? `?${qs}` : ''}`);
	return response.json();
}

export async function adminUpdateUser(
	token: string | null,
	id: number,
	data: Partial<
		Pick<ApiUser, 'first_name' | 'last_name' | 'email' | 'phone_number' | 'national_id' | 'role'>
	>
): Promise<AdminUserRow> {
	const response = await authFetch(token, `/user/admin/users/${id}/`, {
		method: 'PATCH',
		body: JSON.stringify(data)
	});
	return response.json();
}

export async function adminListGroups(token: string | null, q?: string): Promise<AdminGroupRow[]> {
	const response = await authFetch(
		token,
		q ? `/user/admin/groups/?q=${encodeURIComponent(q)}` : '/user/admin/groups/'
	);
	return response.json();
}

export async function adminListTickets(
	token: string | null,
	unresolvedOnly = false
): Promise<Ticket[]> {
	const response = await authFetch(
		token,
		`/user/admin/tickets/${unresolvedOnly ? '?unresolved=1' : ''}`
	);
	return response.json();
}

export async function adminSetTicketResolved(
	token: string | null,
	id: number,
	resolved: boolean
): Promise<Ticket> {
	const response = await authFetch(token, `/user/admin/tickets/${id}/resolve/`, {
		method: 'POST',
		body: JSON.stringify({ resolved })
	});
	return response.json();
}

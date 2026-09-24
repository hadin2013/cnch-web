import { getAuthUser } from '$lib/utils/auth';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = ({ cookies }) => {
	return { auth: getAuthUser(cookies) };
};

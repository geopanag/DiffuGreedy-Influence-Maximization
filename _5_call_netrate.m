
network = '';
for c in {'total_cascades','degree','authority','cascading_outdegree'}
	cascades = strcat('path\to\Data\netrate\cascades_',c,'.txt');
    
    horizon = 10;
	type_diffusion = 'exp';
	num_nodes = 3000;

	tic
	[A_hat, total_obj, pr, mae] = netrate(network, cascades, horizon, type_diffusion, num_nodes);

	csvwrite(strcat('path\to\Data\netrate\network_',c,'.txt'),full(A_hat))
	disp("Done -------------------------------------------------------------")
	disp(toc)
end
<template>
  <div>
    <pf-table :rows="machines" :columns="columns" >
      <template slot-scope="scope">
        <td v-for="attr in columns"> {{scope.row[attr]}} </td>
      </template>
      <slot name="action">
        action
      </slot>
      <slot name="dropdown">
        dropdown
      </slot>
    </pf-table>
  </div>
</template>

<script>
export default {
  data () {
    return {
      columns: [
        'hostname',
        'system-type',
        'expire_time',
        'start_time'
      ],
      machines: [
        {
          'disk-total_size': 152587,
          'cpu-socket_number': 1,
          'cpu-stepping': [
            '5'
          ],
          'hvm': true,
          'meta': {
            'beaker-job-id': 'J:2040774'
          },
          'system-type': 'baremetal',
          'cpu-model': '30',
          'system-vendor': 'NEC',
          'start_time': '2017-09-08T08:51:59',
          'provisioner': 'beaker',
          'cpu-model_name': 'Intel(R) Xeon(R) CPU X3460 @ 2.80GHz',
          'cpu-family': 6,
          'cpu-core_number': 8,
          'hostname': 'nec-em26.rhts.eng.bos.redhat.com',
          'iommu': true,
          'cpu-flag': [
            'aperfmperf',
            'ept',
            'mca',
            'sse4_1',
            'dtes64',
            'pse',
            'mce',
            'msr',
            'tm2',
            'pni',
            'ida',
            'rdtscp',
            'vnmi',
            'cx16',
            'cmov',
            'mtrr',
            'vpid',
            'pae',
            'tsc',
            'pat',
            'fxsr',
            'clflush',
            'rep_good',
            'xtopology',
            'de',
            'nx',
            'nonstop_tsc',
            'sse4_2',
            'dts',
            'ds_cpl',
            'pse36',
            'lahf_lm',
            'pebs',
            'cx8',
            'sse2',
            'vme',
            'fpu',
            'smx',
            'est',
            'pbe',
            'acpi',
            'mmx',
            'tpr_shadow',
            'vmx',
            'ssse3',
            'flexpriority',
            'ht',
            'syscall',
            'monitor',
            'xtpr',
            'sep',
            'ss',
            'constant_tsc',
            'sse',
            'apic',
            'lm',
            'popcnt',
            'tm',
            'pge',
            'bts',
            'pdcm',
            'arch_perfmon'
          ],
          'expire_time': '2017-09-09T08:51:59',
          'numa-node_number': 1,
          'cpu-vendor': 'GenuineIntel',
          'tasks': {
            '5ac8454c-946e-11e7-a16e-f0def1fed532': {
              'status': 'running',
              'type': 'provision'
            }
          },
          'cpu-arch': 'x86_64',
          'memory-total_size': 15942,
          'magic': '9e1e456d-5f28-473f-83af-13fbd6847b74',
          'beaker-distro_family': 'RedHatEnterpriseLinuxAlternateArchitectures7',
          'beaker-distro': 'RHEL-ALT-7.5-20170908.n.0',
          'cpu-speed': 1197,
          'beaker-distro_variant': 'Server',
          'disk-number': 1,
          'system-model': 'Express 5800/T110b',
          'lifespan': 86400
        },
        {
          'disk-total_size': 152587,
          'cpu-socket_number': 1,
          'cpu-stepping': [
            '5'
          ],
          'hvm': true,
          'meta': {
            'beaker-job-id': 'J:2040774'
          },
          'system-type': 'baremetal',
          'cpu-model': '30',
          'system-vendor': 'NEC',
          'start_time': '2017-09-08T08:51:59',
          'provisioner': 'beaker',
          'cpu-model_name': 'Intel(R) Xeon(R) CPU X3460 @ 2.80GHz',
          'cpu-family': 6,
          'cpu-core_number': 8,
          'hostname': 'nec-em25.rhts.eng.bos.redhat.com',
          'iommu': true,
          'cpu-flag': [
            'aperfmperf',
            'ept',
            'mca',
            'sse4_1',
            'dtes64',
            'pse',
            'mce',
            'msr',
            'tm2',
            'pni',
            'ida',
            'rdtscp',
            'vnmi',
            'cx16',
            'cmov',
            'mtrr',
            'vpid',
            'pae',
            'tsc',
            'pat',
            'fxsr',
            'clflush',
            'rep_good',
            'xtopology',
            'de',
            'nx',
            'nonstop_tsc',
            'sse4_2',
            'dts',
            'ds_cpl',
            'pse36',
            'lahf_lm',
            'pebs',
            'cx8',
            'sse2',
            'vme',
            'fpu',
            'smx',
            'est',
            'pbe',
            'acpi',
            'mmx',
            'tpr_shadow',
            'vmx',
            'ssse3',
            'flexpriority',
            'ht',
            'syscall',
            'monitor',
            'xtpr',
            'sep',
            'ss',
            'constant_tsc',
            'sse',
            'apic',
            'lm',
            'popcnt',
            'tm',
            'pge',
            'bts',
            'pdcm',
            'arch_perfmon'
          ],
          'expire_time': '2017-09-09T08:51:59',
          'numa-node_number': 1,
          'cpu-vendor': 'GenuineIntel',
          'tasks': {
            '5ac8454c-946e-11e7-a16e-f0def1fed532': {
              'status': 'running',
              'type': 'provision'
            }
          },
          'cpu-arch': 'x86_64',
          'memory-total_size': 15942,
          'magic': '9e1e456d-5f28-473f-83af-13fbd6847b74',
          'beaker-distro_family': 'RedHatEnterpriseLinuxAlternateArchitectures7',
          'beaker-distro': 'RHEL-ALT-7.5-20170908.n.0',
          'cpu-speed': 1197,
          'beaker-distro_variant': 'Server',
          'disk-number': 1,
          'system-model': 'Express 5800/T110b',
          'lifespan': 86400
        }
      ]
    }
  }
}
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style scoped>
</style>
